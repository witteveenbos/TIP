from __future__ import annotations
from pydantic import BaseModel
from hail.models.enums import MunicipalityIDs
from hail.models.matrix import Matrix, AggregatedMatrix


class StaticMapData(BaseModel):
    stations: dict[str, StationData]
    gm_to_station_share: dict[str, dict[MunicipalityIDs, float | int | None]]


class StationData(BaseModel):
    invoeding: float | int
    afname: float | int


class DynamicMapShare(BaseModel, arbitrary_types_allowed=True):
    station_ids: list[str]
    demand_capacity: AggregatedMatrix
    supply_capacity: AggregatedMatrix
    municipality_share: dict[str, Matrix]

    def aggregate(self, to_aggregate: Matrix) -> AggregatedMatrix:

        agg_matrix = AggregatedMatrix([None] * self.agg_size)
        for i, station_ids in enumerate(self.station_ids):
            # multiply the matrix with the municipality share, masking with None
            masked_for_this_station = (
                to_aggregate * self.municipality_share[station_ids]
            )
            # for this station, sum all the elements that are part of this station
            agg_matrix[i] = masked_for_this_station.sum_element_wise()

        return agg_matrix

    @property
    def agg_size(self):
        return len(self.station_ids)
