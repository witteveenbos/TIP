# %%
import logging
import geopandas as gpd
import pandas as pd
import numpy as np
from itertools import product
from scipy import sparse
from owslib.wfs import WebFeatureService
import json
from shapely.prepared import prep
from pathlib import Path


# code for this function taken from the pypsa eur project
def shapes_to_shapes(orig: gpd.GeoSeries, dest: gpd.GeoSeries) -> sparse.lil_matrix:
    """
    Adopted from vresutils.transfer.Shapes2Shapes()
    """
    orig_prepped = list(map(prep, orig))
    transfer = sparse.lil_matrix((len(dest), len(orig)), dtype=float)

    for i, j in product(range(len(dest)), range(len(orig))):
        if orig_prepped[j].intersects(dest.iloc[i]):
            area = orig.iloc[j].intersection(dest.iloc[i]).area
            transfer[i, j] = area / dest.iloc[i].area

    return transfer


### This was a function, but thats not really usefull when debugging the WFS retrieval with interactive windows
"""
This function maps the total capacity of the substations to the municipalities.
The data is retrieved from the PDOK WFS service.
The total capacity of the substations is then mapped to the municipalities.
The function returns a GeoDataFrame with the municipalities, with two extra columns for the total substation capacity available for invoeding and afname specific to that municipality.

Parameters:
fp_municipalities: Path

Returns:
gdf_municipalities: gpd.GeoDataFrame
gdf_substations: gpd.GeoDataFrame
"""
fp_municipalities = "data/municipalities_simplified.geojson"

# Load the data
gdf_municipalities: gpd.GeoDataFrame = gpd.read_file(fp_municipalities)

# setup of wfs connection
wfs_url = "https://service.pdok.nl/kadaster/netcapaciteit/wfs/v1_0"
wfs = WebFeatureService(url=wfs_url, version="2.0.0")

# List available layers, layer 1 contains the verzorgingsgebieden, layer 0 contains the substations
layers = list(wfs.contents)

### if you want more info:
schema = wfs.get_schema(layers[1])
properties = list(schema.get("properties").keys())

# probe the WFS api and save the response in a GeoDataFrame
response = wfs.getfeature(typename=layers[1], outputFormat="json")
gdf_substations: gpd.GeoDataFrame = gpd.read_file(response)
gdf_substations = gdf_substations.to_crs(gdf_municipalities.crs)

# Cookie cut the substations down to only the province of interest
gdf_substations = gdf_substations.clip(gdf_municipalities)

# compute a transfer matrix between the municipalities and the substations
transfer = shapes_to_shapes(gdf_municipalities.geometry, gdf_substations.geometry)

# select relevant data columns from substations data that we want to map to municipalities
invoeding = "totaleCapaciteitInvoedingMva"
afname = "totaleCapaciteitAfnameMva"
gdf_substations["unit"] = 1
# apply operation:
gdf_municipalities["invoeding"] = transfer.T.dot(gdf_substations[invoeding])
gdf_municipalities["afname"] = transfer.T.dot(gdf_substations[afname])

gdf_municipalities, gdf_substations
# end of function


VISUAL_VALIDATION = True

transfer_matrix = shapes_to_shapes(
    gdf_substations.geometry, gdf_municipalities.geometry
)
transfer_matrix = transfer_matrix.toarray()

## Create a mapper that divides the load per municipality over the overlapping stations
mapper = {}
for i, row in enumerate(transfer_matrix):

    this_region = gdf_municipalities.iloc[i]["identificatie"]

    # make the map
    mapper.update(
        {
            this_region: {
                station_id: float(value)
                for station_id, value in zip(gdf_substations.station, row)
            }
        }
    )
# %%

# assure that regions are correctly split and not more than their actual load is split
for region, station_dict in mapper.items():
    assert round(sum(station_dict.values()), 1) <= 1.0

# flip the mapper so that we have a station to region map
flipped_mapper = {}
for top_key, nested_dict in mapper.items():
    for nested_key, value in nested_dict.items():
        if nested_key not in flipped_mapper:
            flipped_mapper[nested_key] = {}
        flipped_mapper[nested_key][top_key] = value


# remove the stations that are not relevant (less than 5% of the total load of a municipality)
flipped_mapper = {k: v for k, v in flipped_mapper.items() if sum(v.values()) > 0.02}


# %%
try:
    gdf_substations.set_index("station", inplace=True)
except KeyError:
    pass
hsms = (
    gdf_substations.loc[flipped_mapper.keys()]
    .copy()
    .reset_index()[
        [
            "station",
            "geometry",
            "totaleCapaciteitInvoedingMva",
            "totaleCapaciteitAfnameMva",
        ]
    ]
    .rename(
        columns={
            "station": "name",
            "totaleCapaciteitInvoedingMva": "invoeding",
            "totaleCapaciteitAfnameMva": "afname",
        }
    )
)

# %%

if VISUAL_VALIDATION:
    for station_name, relation_to_municipalities in flipped_mapper.items():

        this_station = hsms[hsms["name"] == station_name]

        ax = this_station.plot()
        for code, value in relation_to_municipalities.items():
            if value > 0.01:
                this_region = gdf_municipalities[gdf_municipalities["identificatie"] == code]
                this_region.plot(
                    ax=ax,
                    color="red",
                    alpha=0.5,
                    linewidth=0.5,
                    edgecolor="black",
                )
                ax.annotate(
                    f"{value:.2f}",
                    (
                        this_region.geometry.centroid.x,
                        this_region.geometry.centroid.y,
                    ),
                )
                # remove all axis
                ax.axis("off")
                # set the title
                ax.set_title(f"{station_name}")

                output_dir = Path("visual_checks/per_station/")
                output_dir.mkdir(parents=True, exist_ok=True)
                fig = ax.get_figure()
                fig.savefig(output_dir / f"{station_name}.png")

# %%

# save the mapper
with open("data/municipal_load_to_station_map.json", "w") as f:
    json.dump(flipped_mapper, f)


# save only the capacities
hsms_fordict = hsms[["name", "invoeding", "afname"]]
with open("data/hsms_capacity.json", "w") as f:
    hsms_d = hsms_fordict.to_dict("records")
    hsms_d = {d["name"]: {k: v for k, v in d.items() if k != "name"} for d in hsms_d}
    json.dump(hsms_d, f)

# save the shapes
hsms["label"] = hsms["name"]
hsms["gid"] = hsms["name"]
hsms.drop("name", axis=1, inplace=True)
hsms = hsms[["label", "gid", "geometry"]]
hsms.to_file("data/hsms.geojson", driver="GeoJSON")
