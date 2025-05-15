from pydantic import BaseModel, Field
from typing import Any, Optional

from hail.development import AbstractDevelopment
from hail.models.configuration import (
    AccessedAttributes,
    AggregationConfig,
    DistributedScenarioRelation,
)
from hail.models.scenario import ScenarioDisplay
from hail.result import AbstractResultMap
from hail.result.graph import AbstractResultGraph


class PreloadedState(BaseModel, arbitrary_types_allowed=True):
    mapclasses: Optional[list[AbstractResultMap]] = None
    graphclasses: Optional[list[AbstractResultGraph]] = None
    developmentclasses: Optional[list[AbstractDevelopment]] = None
    accessed_attributes: Optional[AccessedAttributes] = None
    scenario_display: Optional[list[ScenarioDisplay]] = None
    scenario_relations: Optional[list[DistributedScenarioRelation]] = None
    aggregation_configs: Optional[list[AggregationConfig]] = None

    is_immutable: bool = Field(default=False, exclude=True)

    def __setattr__(self, name: str, value: Any) -> None:
        if self.is_immutable and name not in {"is_immutable"}:
            raise TypeError("This model is immutable and cannot be modified.")
        super().__setattr__(name, value)

    def make_immutable(self) -> None:
        object.__setattr__(self, "is_immutable", True)
