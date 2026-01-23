from __future__ import annotations
import logging
from typing import Any, Literal, Optional
import colorcet as cc
from pydantic import BaseModel

from hail.models.enums import (
    AllAreaDivisionIDs,
    plotTypes,
)
from hail.models.fundamental import Value
from hail.models.matrix import AggregatedMatrix, Matrix
from hail.util import get_color


class NullReponse(BaseModel):
    component: Literal["developments", "map", "graph"]
    msg: str


class CalculateResponse(BaseModel):
    input: Optional[InputResponse] = None
    map: Optional[MapResponse] = None
    graph: Optional[GraphResponse] = None
    msgs: Optional[list[NullReponse]] = None


# ------ > Map
class MapResponse(BaseModel):
    metadata: MapMetaData
    mapData: dict[AllAreaDivisionIDs, MapDataEntry]  # type: ignore


class LegendLabel(BaseModel):
    label: str
    color: str


class MapMetaData(BaseModel):
    legendTitle: str
    unit: str
    legendLabels: list[LegendLabel]


class MapDataEntry(BaseModel):
    gid: AllAreaDivisionIDs
    value: float | int | None  # TODO: should not accept None
    color: str


class LegendDef(BaseModel):
    steps: int
    decimals: int = 2


class ColorMapDef(BaseModel):
    colormap: str
    reverse: bool = False
    # if True, the colormap will be reversed
    lower_limit: Optional[float | int] = None
    # if None, the minimum value of the data is used
    upper_limit: Optional[float | int] = None
    # if None, the maximum value of the data is used

    def get_color_for_value(self, value: float | int) -> str:
        if self.lower_limit is None or self.upper_limit is None:
            raise ValueError(
                "[colormap]: Lower and upper limit should be set before getting a color (use `set_limits`)"
            )
        return get_color(
            value=value,
            cmap_name=self.colormap,
            vmin=self.lower_limit,
            vmax=self.upper_limit,
            reverse=self.reverse,
        )

    def model_post_init(self, __context: Any) -> None:
        # ensure that the colormap is a valid colormap for cc
        if not hasattr(cc, self.colormap):
            raise ValueError(
                f"Colormap '{self.colormap}' is not a valid colormap for colorcet"
            )

        if not self.colormap.startswith("b"):
            raise ValueError(
                f"Colormap should have a 'b' prefix to get hex output (input: '{self.colormap}')"
            )

        return super().model_post_init(__context)

    def set_limits(self, matrix: Matrix | AggregatedMatrix) -> None:
        if self.lower_limit is None:
            self.lower_limit = min(matrix)
            logging.debug(f"Setting lower limit to {self.lower_limit}")
        else:
            logging.debug("Not overwriting the existing lower limit")
        if self.upper_limit is None:
            self.upper_limit = max(matrix)
            logging.debug(f"Setting upper limit to {self.upper_limit}")
        else:
            logging.debug("Not overwriting the existing higher limit")


# ------ > Input
class DevelopmentElement(BaseModel):
    key: str
    name: str
    min: float | int
    max: float | int
    default: float | int
    unit: str


class DevelopmentGroup(BaseModel):
    key: str
    name: str
    type: str
    inputs: list[DevelopmentElement]

    def __hash__(self):
        return hash((self.key, self.name, self.type))

    def __eq__(self, other):
        if not isinstance(other, DevelopmentGroup):
            return False
        return (
            self.key == other.key
            and self.name == other.name
            and self.type == other.type
        )


#  as used for the continous developments
ContinuousDevSetting = float | int


InputResponse = dict[AllAreaDivisionIDs, list[DevelopmentGroup]]


# as used for the sectoral developments
class SectoralDevSetting(BaseModel):
    type: str
    value: float | int


class UpdatedInputElement(DevelopmentElement):
    user_values: ContinuousDevSetting | list[SectoralDevSetting]


class UpdatedInputGroup(DevelopmentGroup):
    inputs: Optional[list[UpdatedInputElement]] = None


# ------ > Graph
class GraphResponse(BaseModel):
    metaData: GraphMeta
    graphData: list[GraphElement]


class GraphMeta(BaseModel):
    title: str = "default"
    unit: str = "default"
    yLabelText: str
    plotType: plotTypes
    xLabelText: Optional[str] = None
    xGrouping: Optional[Groupable] = None


class GraphElement(BaseModel, arbitrary_types_allowed=True):
    carrier: str
    sector: str
    demandSupply: str
    color: str
    value: float | int | Matrix

    def filter_on_index(self, index: int) -> GraphElement:
        assert isinstance(
            self.value, Matrix
        ), "Cannot filter on index if value is not a matrix"
        return GraphElement(
            carrier=self.carrier,
            sector=self.sector,
            demandSupply=self.demandSupply,
            color=self.color,
            value=self.value[index],
        )


Groupable = Literal["sector", "carrier", "demandSupply"]


class ETMSetter(BaseModel, arbitrary_types_allowed=True):
    key: str
    value: Value
