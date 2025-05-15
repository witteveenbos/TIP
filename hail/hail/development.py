from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import logging
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ValidationError

from hail.context import ContextProvider
from hail.models.fundamental import FilterList
from hail.models.matrix import AggregatedMatrix, Matrix
from hail.models.calculate import ETMSetter, DevelopmentGroup, DevelopmentElement
from hail.models.response import InputResult
from hail.models.enums import AllAreaDivisionIDs
from hail.util import id_to_region_map


class DevelomentType(Enum):
    SECTORAL = "sectoral"
    CONTINUOUS = "continuous"


class Group(BaseModel):
    name: str
    key: str
    _context: Optional[ContextProvider] = None
    _members: Optional[set[AbstractDevelopment]] = set()

    def _add_member(self, member: AbstractDevelopment):
        self._members.add(member)

    def add_context(self, context: ContextProvider):
        self._context = context

    def __hash__(self):
        return hash((self.name, self.key))

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return self.name == other.name and self.key == other.key

    def __str__(self):
        return self.key

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def TOTAL(self) -> str:
        var = self._context
        return sum([getattr(var.ui, member.key) for member in self._members])


class AbstractDevelopment(ABC):

    @property
    @abstractmethod
    def group(self) -> Group | None:
        pass

    @property
    @abstractmethod
    def key(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @property
    @abstractmethod
    def dev_type(self) -> DevelomentType:
        pass

    @property
    @abstractmethod
    def max(self) -> Matrix:
        pass

    @property
    @abstractmethod
    def min(self) -> Matrix:
        pass

    @property
    @abstractmethod
    def default(self) -> Matrix:
        pass

    @property
    @abstractmethod
    def sets_ETM_value(self) -> Matrix:
        pass

    @property
    @abstractmethod
    def aggregate(self) -> Matrix:
        pass

    @classmethod
    def determine_etm_setters(
        cls, context: ContextProvider
    ) -> list[list[Optional[ETMSetter]]]:

        value: dict[FilterList[InputResult], Matrix] = cls.sets_ETM_value(context)
        result = []

        # enter row wise (setters, scenario wide)
        for lhs, rhs in value.items():
            this_setter = []

            # type hint
            if TYPE_CHECKING:
                lhs: FilterList[InputResult] = lhs
                rhs: Matrix = rhs

            key_to_set = lhs.etm_key

            # enter column wise (scenarios, matrix wide)
            # return ETMSetter for each scenario where Matrix is not None
            for matrix_value in rhs:
                if matrix_value is not None:
                    this_setter.append(
                        ETMSetter(
                            key=key_to_set,
                            value=matrix_value,
                        )
                    )
                else:
                    this_setter.append(None)

            result.append(this_setter)

        return result

    @classmethod
    def make_developments(
        cls, context: ContextProvider
    ) -> dict[str, list[DevelopmentGroup]]:
        default_values = cls.default(context)

        id_to_region = id_to_region_map(request=context.request)
        region_ids = [id_to_region[scenario_id] for scenario_id in context.scenario_ids]

        return cls.compute_developments(
            context=context, default_values=default_values, region_ids=region_ids
        )

    @classmethod
    def make_developments_aggregate(
        cls, context: ContextProvider
    ) -> dict[str, list[DevelopmentGroup]]:

        aggregator = context.aggregator
        to_aggretate = cls.aggregate(context)
        agg_default_values = aggregator.aggregate(
            to_aggregate=to_aggretate, context=context
        )

        return cls.compute_developments(
            context=context,
            default_values=agg_default_values,
            region_ids=aggregator.region_ids,
        )

    @classmethod
    def compute_developments(
        cls,
        context: ContextProvider,
        default_values: Matrix | AggregatedMatrix,
        region_ids: list[AllAreaDivisionIDs],
    ) -> dict[str, list[DevelopmentGroup]]:

        min_values = cls.min(context)
        max_values = cls.max(context)
        key = cls.key
        name = cls.name
        unit = cls.unit
        group: Group = cls.group
        development_type: DevelomentType = cls.dev_type

        try:
            dev = {
                region_id: [
                    DevelopmentGroup(
                        key=group.key,
                        name=group.name,
                        type=development_type,
                        inputs=[
                            DevelopmentElement(
                                key=key,
                                name=name,
                                min=min_value,
                                max=max_value,
                                default=default_value,
                                unit=unit,
                            )
                        ],
                    )
                ]
                for region_id, min_value, max_value, default_value in zip(
                    region_ids, min_values, max_values, default_values
                )
            }
            return dev
        except ValidationError:
            logging.info(f"Error in development group creation: {key}")
