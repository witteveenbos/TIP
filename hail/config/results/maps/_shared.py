from __future__ import annotations
import json
import logging
from pathlib import Path
from hail.models.calculate import ColorMapDef, MapDataEntry, MapResponse
from hail.models.map import StaticMapData, StationData, DynamicMapShare
from hail.models.matrix import AggregatedMatrix, Matrix
from hail.util import id_to_region_map
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from hail.context import ContextProvider
    from hail.result.map import AbstractResultMap

# TODO: make sure this is only done on initial load
DATA = Path(__file__).parent / "data"
with open(DATA / "hsms_capacity.json") as f:
    hsms_capacity = json.load(f)

with open(DATA / "municipal_load_to_station_map.json") as f:
    gm_to_station_share = json.load(f)
## ^^

STATIC_MAP_DATA = StaticMapData(
    stations={
        name: StationData(invoeding=station["invoeding"], afname=station["afname"])
        for name, station in hsms_capacity.items()
    },
    # replace 0.0 with None
    gm_to_station_share={
        name: {
            gmid: (this_share if this_share != 0.0 else None)
            for gmid, this_share in share.items()
        }
        for name, share in gm_to_station_share.items()
    },
)


def get_dynamic_map_share(context: ContextProvider) -> DynamicMapShare:
    """This orders the static data in the same way as the incoming request"""
    region_map = id_to_region_map(context.request)
    regions_ordered = [region_map[scen_id] for scen_id in context.scenario_ids]
    demand_cap = []
    supply_cap = []
    station_ids = []
    municipality_share = {}
    for station_id, station_data in STATIC_MAP_DATA.stations.items():
        station_ids.append(station_id)
        demand_cap.append(station_data.afname)
        supply_cap.append(station_data.invoeding)

        this_station_str_map = {
            enum.value: value
            for enum, value in STATIC_MAP_DATA.gm_to_station_share[station_id].items()
        }

        municipality_share[station_id] = Matrix(
            [this_station_str_map[region] for region in regions_ordered]
        )

    return DynamicMapShare(
        station_ids=station_ids,
        demand_capacity=AggregatedMatrix(demand_cap),
        supply_capacity=AggregatedMatrix(supply_cap),
        municipality_share=municipality_share,
    )


def determine_used_capacity(
    cls: AbstractResultMap,
    var: ContextProvider,
    field_name: Literal["demand_capacity", "supply_capacity"],
) -> tuple[Matrix, DynamicMapShare]:

    peak_load: Matrix = cls.map_aggregate(var=var)
    dynamic_map_share = get_dynamic_map_share(context=var)
    agg_peak_load = dynamic_map_share.aggregate(peak_load)
    relevant_capacity = getattr(dynamic_map_share, field_name)
    if relevant_capacity is None:
        raise ValueError(f"{field_name} is not set in 'DynamicMapShare'")

    used_capacity = agg_peak_load / relevant_capacity * 100

    # TODO: check if this is the correct way to calculate the used capacity

    return used_capacity, dynamic_map_share


def make_grid_map(
    cls: AbstractResultMap,
    var: ContextProvider,
    field_name: Literal["demand_capacity", "supply_capacity"],
) -> MapResponse:
    used_capacity, dynamic_map_share = determine_used_capacity(
        cls=cls, var=var, field_name=field_name
    )
    # TODO: check why we don't have type safety here
    cm: ColorMapDef = cls.make_colormap(map_matrix=used_capacity)
    map_metadata = cls._make_metadata(colormap=cm)

    this_map = {
        station_id: MapDataEntry(
            gid=station_id,
            value=value,
            color=cm.get_color_for_value(value),
        )
        for station_id, value in zip(dynamic_map_share.station_ids, used_capacity)
    }
    return MapResponse(
        metadata=map_metadata,
        mapData=this_map,
    )
