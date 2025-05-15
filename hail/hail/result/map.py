from __future__ import annotations
from abc import abstractmethod
from copy import copy
import logging
from typing import TYPE_CHECKING

from hail.context import ContextProvider
from hail.models.calculate import (
    ColorMapDef,
    LegendDef,
    LegendLabel,
    MapDataEntry,
    MapMetaData,
    MapResponse,
)
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.models.matrix import AggregatedMatrix, Matrix
from hail.util import linspace, id_to_region_map
from hail.result.base import AbstractResult


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResultMap(AbstractResult):

    @property
    @abstractmethod
    def colormap(self) -> ColorMapDef:
        pass

    @property
    @abstractmethod
    def legend(self) -> LegendDef:
        pass

    @property
    @abstractmethod
    def related_carrier(self) -> CarrierEnum:
        pass

    @property
    @abstractmethod
    def related_balance(self) -> BalanceEnum:
        pass

    @property
    def related_area_div(self) -> AreaDivisionEnum | list[AreaDivisionEnum] | None:
        return None

    @abstractmethod
    def map(self, var: Var) -> Matrix:
        pass

    @property
    @abstractmethod
    def map_aggregate(self, var: Var) -> Matrix:
        pass

    @classmethod
    def make_colormap(cls, map_matrix: Matrix | None = None) -> ColorMapDef:
        """
        Since we use class variables, we need to make a copy of the colormap definition.
        Otherwise, the limits would be set for all instances of the class.
        """
        # make a copy of the colormap definition
        cm = ColorMapDef(**cls.colormap.model_dump())
        # set the limits on that colormap
        if map_matrix is not None:
            cm.set_limits(map_matrix)
        return cm

    @classmethod
    def _make_metadata(cls, colormap: ColorMapDef) -> MapMetaData:
        cm = colormap
        legend: LegendDef = cls.legend
        return MapMetaData(
            legendTitle=cls.name,
            unit=cls.unit,
            legendLabels=[
                LegendLabel(
                    label=f"{value} {cls.unit}", color=cm.get_color_for_value(value)
                )
                for value in linspace(
                    start=cm.lower_limit,
                    stop=cm.upper_limit,
                    num=legend.steps,
                    decimals=legend.decimals,
                )
            ],
        )

    @classmethod
    def make_map(cls, context: ContextProvider) -> MapResponse:
        map_matrix: Matrix = cls.map(context)
        cm = cls.make_colormap(map_matrix=map_matrix)
        map_metadata = cls._make_metadata(colormap=cm)
        id_to_region = id_to_region_map(request=context.request)
        this_map = {
            id_to_region[scen_id]: MapDataEntry(
                gid=id_to_region[scen_id],
                value=value,
                color=cm.get_color_for_value(value),
            )
            for scen_id, value in zip(context.scenario_ids, map_matrix)
        }
        return MapResponse(
            metadata=map_metadata,
            mapData=this_map,
        )

    @classmethod
    def make_map_aggregate(cls, context: ContextProvider) -> MapResponse:

        # this should yield the (normalized) map data to aggregate
        map_matrix: Matrix = cls.map_aggregate(context)

        # get the relevant aggregation from the context
        aggregator = context.aggregator

        # calculate the aggregated matrix
        agg_matrix = aggregator.aggregate(to_aggregate=map_matrix, context=context)

        cm = cls.make_colormap(map_matrix=agg_matrix)
        map_metadata = cls._make_metadata(colormap=cm)
        this_map = {
            region: MapDataEntry(
                gid=region,
                value=value,
                color=cm.get_color_for_value(value),
            )
            for region, value in zip(aggregator.region_ids, agg_matrix)
        }
        return MapResponse(
            metadata=map_metadata,
            mapData=this_map,
        )
