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

## shapes_mapper_grid_only.py

- Restored the `pmiek_substation_mapper` function expected by the visualisation scripts.
- Moved mapper execution behind a `__main__` guard so importing the module does not immediately read files, create plots or overwrite output files.
- Kept capacity mapping and station-to-municipality overlap fractions in EPSG:28992, avoiding area calculations in geographic degrees.
- Added validation for required input fields and a clear error when the municipality and station layers do not overlap.
- Made per-station visual validation and `municipal_load_to_station_map.json` generation optional for callers.
- The standalone mapper uses the legacy Noord-Holland municipality source because the checked-in `hsms.geojson` and `hsms_capacity.json` contain Noord-Holland station data.

## shapes_visuals.py

- Uses the restored mapper function instead of importing a function that no longer existed.
- Uses the matching legacy Noord-Holland municipality layer for visual comparisons with the current station data.
- Uses the shared project data paths from `constants.py`.

Run the mapper or visualisation with Poetry:

```powershell
poetry run python shapes_mapper_grid_only.py
poetry run python shapes_visuals.py
```

## constants.py

Added constants for the project paths which can be reused by multiple scripts.