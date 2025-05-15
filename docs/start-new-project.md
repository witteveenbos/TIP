## (1) Prepare grid GIS-data with VIVET
https://gitlab.wbad.witteveenbos.com/energy-modeling/vivet-pmiek

1. [Download](https://www.pdok.nl/atom-downloadservices/-/article/bestuurlijke-grenzen) municipalities geoshapes, add to `/data` folder as `municipalities_simplified.geojson` 
> Might be useful to also make this work as a script function
2. Run `geomapping_regions.py` to generate the relational mapping between municipalities, RES-regions and provinces to create `geo_mapping.csv`
3. Run `shapes_mapper_grid_only.py` to generate the relational mapping between municipality loads and the substations
4. [optional] if you want you can check the results visually by running `shapes_visuals.py`
5. You should now have the following files:
   1. `geo_mapping.csv`
   1. `hsms_capacity.json`
   1. `hsms.geojson`
   1. `hsms.min.geojson`
   1. `municipal_load_to_station_map.json`
   1. `municipalities_simplified.geojson`
   1. `municipalities_to_province.json`
   1. `municipalities_to_region.json`
   1. `municipalities_to_res.json`
6. ???
7. ✅

## Add/change geoshapes in webapp (Django backend)
1. [Download](https://www.pdok.nl/atom-downloadservices/-/article/bestuurlijke-grenzen) geoshapes, 
2. (Simplify them)
3. Add to `src/energy/static/shapes` folder as:
    1. `municipalities_simplified.geojson`
    2. `municipalities.geojson`
    3. `province_simplified.geojson`
    4. `province.geojson`
    5. `regions_simplified.geojson`
    6. `regions.geojson`
    7. `res_simplified.geojson`
    8. `res.geojson`
4. From (1) copy these files to the same folder:
   1. `hsms.geojson`
   2. `hsms.min.geojson`

## (2) Regionalize ETM-scenarios (Quintel in ETM using ETM scenario tools)
1. Get data
2. Do thing
3. Be Quintel
4. Result: excel sheet like `data/scenario_links.xlsx` but for this province

## Update aggregation and ETM-scenario JSONs in Hail microservice

### Configuring ETM-scenarios
1. Add the results of (2) to `data/scenario_links.xlsx`
2. Run `data/parse_links.py` to generate JSONs that relate the national scenario to municipal ETM scenarios in the `config/scenarios` folder
3. By hand (or AI) update the `scenario-list.json` file in the `config/scenarios` folder so that for every of the main scenarios, a Title and Description exists

### Configuring area divisions and relationships
1. Add the results of (1) to `config/data`
   1. `municipalities_to_province.json`
   1. `municipalities_to_region.json`
   1. `municipalities_to_res.json`
2. Add the results of (1) to `config/results/maps/data`
   1. `hsms_capacity.json`
   1. `municipal_load_to_station_map.json`


## 🚀➡️☁️ Deploy to the cloud! Hyperscaling!
1. Deploy 2 container services on Azure, one for the webapp and one for the microservice
2. Set all the env variables (like domain pointing between both services)
3. ???
4. ✅