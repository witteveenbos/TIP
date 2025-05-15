
# Warn that this assumes this data structure
# data/
# ├── hsms_capacity.json
# ├── hsms.min.geojson
# ├── municipalities_to_province.json
# ├── municipalities_to_region.json
# ├── municipal_load_to_station_map.json

# top_folder/ (one level above this repo)
# ├── data/ (microservice)
# ├── tool/ (webapp)
# ├── gis/ (this repo)

echo """
This script assumes the following data structure:
top_folder/ (one level above this repo)
├── data/ (microservice)
├── tool/ (webapp)
├── gis/ (this repo)
"""


## To the webapp
sudo cp data/hsms.min.geojson ../tool/src/energy/static/shapes/hsms.geojson

## To the microservice

# station capacity
sudo cp data/hsms_capacity.json ../data/config/results/maps/data/

# share maps
sudo cp data/municipal_load_to_station_map.json ../data/config/results/maps/data/
sudo cp data/municipalities_to_province.json ../data/config/results/maps/data/
sudo cp data/municipalities_to_res.json ../data/config/results/maps/data/
sudo cp data/municipalities_to_region.json ../data/config/results/maps/data/