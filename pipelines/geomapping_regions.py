import json
import logging

import pandas as pd

from constants import DATA_DIR

LOGGER = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


df = pd.read_csv(DATA_DIR / "geo_mapping.csv")[["Municipality_ID", "Region_ID", "RES_ID", "Provincie_ID"]]

df.set_index("Municipality_ID", inplace=True)
LOGGER.info(f"Loaded {len(df)} municipality mappings from {DATA_DIR / 'geo_mapping.csv'}")


all_maps = []
for area_div in ["Region_ID", "RES_ID", "Provincie_ID"]:
    area_map = {}
    for region, gdf in df.groupby(area_div):
        area_map[region] = {k: 1 for k in gdf.index.tolist()}

    all_maps.append(area_map)
    LOGGER.info(f"Built {len(area_map)} {area_div} mappings")

for map in all_maps:

    # add all municipalities with 0 if not already in the map
    for k in map.keys():
        for m in df.index:
            if m not in map[k]:
                map[k][m] = 0

    # assert that all municipalities are in the map, summing to 52
    value = sum(sum(v.values()) for v in map.values())
    if value != len(df.index):
        LOGGER.error(f"Invalid mapping total: {value}, expected {len(df.index)}")
    assert value == len(df.index), f"Value is {value} expected {len(df.index)}"

for map, level in zip(all_maps, ["region", "res", "province"]):
    output_path = DATA_DIR / f"municipalities_to_{level}.json"
    with output_path.open("w") as f:
        json.dump(map, f)
    LOGGER.info(f"Wrote {len(map)} {level} mappings to {output_path}")
