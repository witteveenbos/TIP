from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel

from hail.models.enums import AreaDivisionEnum, MainScenarioEnum, AllAreaDivisionIDs
from hail.models.fundamental import Value
from hail.models.matrix import AggregatedMatrix, Matrix
from hail.models.request import MunicipalityScenario
import logging
from typing import TYPE_CHECKING

from hail.util import id_to_region_map, region_to_id_map

if TYPE_CHECKING:
    from hail.context import ContextProvider


class DistributedScenarioRelation(BaseModel):
    main_scenario: MainScenarioEnum
    municipal_scenarios: list[MunicipalityScenario]

    @classmethod
    def multiple_from_config(
        cls, config_folder_path: Path
    ) -> list[DistributedScenarioRelation]:
        multiple = []
        for file in config_folder_path.glob("scenarios/ii3050*.json"):
            obj = cls.from_config(file)
            multiple.append(obj)
        if len(multiple) == 0:
            raise ValueError(
                "Could not find any valid ii3050*.json files in 'config/scenarios/' (obj: hail.models.scenario.DistributedScenarioRelation) "
            )
        return multiple

    @staticmethod
    def from_config(file_path: Path) -> DistributedScenarioRelation:
        with open(file_path) as f:
            try:
                data = json.load(f)
                return DistributedScenarioRelation(**data)
            except Exception as e:
                logging.debug("Skipping as could not parse file %s", file_path.stem)
                logging.debug(e)


class ETMScenario(BaseModel):
    name: str
    etm_id: int

    @property
    def url_path(self):
        return f"/api/v3/scenarios/{self.etm_id}"

    user_values: Optional[dict[str, Value]] = None
    selectedScenario: Optional[MainScenarioEnum] = None


class AggregationConfig(BaseModel):
    area_division: AreaDivisionEnum
    file_path: str

    share_map: Optional[dict[AllAreaDivisionIDs, float | int | None]] = None
    _region_ids: Optional[list[AllAreaDivisionIDs]] = None

    def load(self, configpath: Path) -> None:
        with open(configpath / self.file_path) as f:
            data = json.load(f)
            self.share_map = data

    def aggregate(
        self, to_aggregate: Matrix, context: ContextProvider
    ) -> AggregatedMatrix:
        """Aggregates the matrix according to the share map of the aggregation config"""

        agg_matrix = AggregatedMatrix([None] * self.agg_size)

        for i, region_id in enumerate(self.region_ids):
            # multiply the matrix with the municipality share, masking with None
            regional_share_matrix = self.get_ordered_share_matrix(
                agg_region=region_id,
                regional_share_map=self.share_map[region_id],
                context=context,
            )
            masked_for_this_region = to_aggregate * regional_share_matrix
            # for this region, sum all the elements that are part of this region
            agg_matrix[i] = masked_for_this_region.sum_element_wise()

        return agg_matrix

    @property
    def agg_size(self):
        return len(self.share_map.keys())

    @property
    def region_ids(self):
        if self._region_ids is None:
            # we need this to be a list to guarantee order
            self._region_ids = list(self.share_map.keys())

        return self._region_ids

    def get_ordered_share_matrix(
        self,
        agg_region: AllAreaDivisionIDs,
        regional_share_map: dict[AllAreaDivisionIDs, float | int | None],
        context: ContextProvider,
    ) -> Matrix:
        """
        Returns the ordered share matrix for the aggregation config,
        stores it since we can share it between components
        """
        # TODO: We can can probably make this a background task,
        # and store it in the cache because it is static over a session

        try:
            # if we have already calculated the ordered share matrix, return it
            ordered_share_matrix = context.ordered_share_matrices[agg_region]

        except KeyError:
            # if we haven't, calculate it and store it in the context
            id_to_region = id_to_region_map(context.request)
            ordered_share_matrix = context.Matrix(None)

            for idx, scenario_id in enumerate(context.scenario_ids):
                this_region = id_to_region[scenario_id]  # these are the gm regions
                ordered_share_matrix[idx] = regional_share_map[
                    this_region
                ]  # that we insert in the right order, based on the scenario id order

            context.ordered_share_matrices[agg_region] = ordered_share_matrix

        return ordered_share_matrix


class AccessedAttributes(BaseModel):
    _ui: set = set()
    _inputs: set = set()
    _gqueries: set = set()

    def __add__(self, other: AccessedAttributes) -> AccessedAttributes:
        self._ui.update(other._ui)
        self._inputs.update(other._inputs)
        self._gqueries.update(other._gqueries)
        return self

    @property
    def ui(self):
        """Sorted list of accessed UI attributes, important for consistent cache key generation"""
        return sorted(list(self._ui))

    @property
    def inputs(self):
        """Sorted list of accessed input attributes, important for consistent cache key generation"""
        return sorted(list(self._inputs))

    @property
    def gqueries(self):
        """Sorted list of accessed gquery attributes, important for consistent cache key generation"""
        return sorted(list(self._gqueries))

    @property
    def private_model_fields_names(self):
        return ["_ui", "_inputs", "_gqueries"]

    def __str__(self):
        return f"AccessedAttributes(ui={self.ui}, inputs={self.inputs}, gqueries={self.gqueries})"

    def __repr__(self):
        return str(self)
