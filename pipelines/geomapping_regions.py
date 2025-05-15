import pandas as pd
import json


df = pd.read_csv("data/geo_mapping.csv")[
    ["Municipality_ID", "Region_ID", "RES_ID", "Provincie_ID"]
]

df.set_index("Municipality_ID", inplace=True)


all_maps = []
for area_div in ["Region_ID", "RES_ID", "Provincie_ID"]:
    area_map = {}
    for region, gdf in df.groupby(area_div):
        area_map[region] = {k: 1 for k in gdf.index.tolist()}

    all_maps.append(area_map)

for map in all_maps:

    # add all municipalities with 0 if not already in the map
    for k in map.keys():
        for m in df.index:
            if m not in map[k]:
                map[k][m] = 0

    # assert that all municipalities are in the map, summing to 52
    value = sum(sum(v.values()) for v in map.values())
    assert value == len(df.index), f"Value is {value} expected {len(df.index)}"

for map, level in zip(all_maps, ["region", "res", "province"]):
    with open(f"data/municipalities_to_{level}.json", "w") as f:
        json.dump(map, f)
