# TIP pipelines

Collection of scripts to load and transform the data required to start an instance of TIP for a new project.


*More documentation will follow later; for now refer to ['start a new project'](../docs/start-new-project.md)*


# Changes for GRDR

## geo_preprocessing.py

- Updated municipality handling from the old index field to the GRDR naam field.
- Kept all spatial calculations and clipping in EPSG:28992, where overlap areas are meaningful.
- Converted every generated GeoJSON to OGC:CRS84 for frontend compatibility.
- Removed the stale hardcoded GM1598 geometry workaround.
- Added path handling relative to the script location.
- Added validation for the configured province and changed the default to Groningen, because the current GRDR source contains only Groningen and Drenthe.
- Preserved generation of both municipalities.geojson and municipalities_simplified.geojson.
## constants.py

Added constants for the project paths which can be reused by multiple scripts.