from hail.models.configuration import AggregationConfig
from hail.models.enums import AreaDivisionEnum


"""
This file contains the configuration for the aggregation of the data.
    1. It should be placed at the root of the config directory. 
    2. File paths are relative to the root of the config directory.
"""

configs = [
    AggregationConfig(
        area_division=AreaDivisionEnum.RES, file_path="data/municipalities_to_res.json"
    ),
    AggregationConfig(
        area_division=AreaDivisionEnum.REG,
        file_path="data/municipalities_to_region.json",
    ),
    AggregationConfig(
        area_division=AreaDivisionEnum.PROV,
        file_path="data/municipalities_to_province.json",
    ),
]
