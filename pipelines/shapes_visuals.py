from pathlib import Path
import logging

import folium
import geopandas as gpd

from constants import BASE_DATA_DIR, DATA_DIR
from shapes_mapper_grid_only import pmiek_substation_mapper

if __name__ == "__main__":
    LOGGER = logging.getLogger(__name__)
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    legacy_municipalities_path = BASE_DATA_DIR / "gemeenten_grdr.geojson"
    gdf_municipalities, gdf_substations = pmiek_substation_mapper(municipalities_path=legacy_municipalities_path)
    LOGGER.info(
        f"Loaded mapped visualisation data for {len(gdf_municipalities)} "
        f"municipalities and {len(gdf_substations)} substations"
    )

    # exclude rotterdam from the plot
    gdf_municipalities: gpd.GeoDataFrame = gdf_municipalities[gdf_municipalities["label"] != "Rotterdam"]
    fig1 = gdf_municipalities.plot(column="invoeding", legend=True)

    gdf_substations_clip: gpd.GeoDataFrame = gdf_substations.clip(gdf_municipalities.total_bounds)
    fig2 = gdf_substations_clip.plot(column="totaleCapaciteitInvoedingMva", legend=True)
    gdf_municipalities.boundary.plot(ax=fig2, color="black")

    # %%
    stations: gpd.GeoDataFrame = gpd.read_file(DATA_DIR / "hsms_grdr.geojson")
    municipalities: gpd.GeoDataFrame = gdf_municipalities

    m = folium.Map(location=[52.1, 5.1], zoom_start=8)
    LOGGER.info("Created Folium map with station and municipality layers")

    # Add stations to the map
    folium.GeoJson(
        stations,
        name="Stations",
        style_function=lambda x: {
            "color": "red",
            "fillOpacity": 0.2,
            "opacity": 0.3,
        },
    ).add_to(m)

    # Add municipalities to the map
    folium.GeoJson(
        municipalities,
        name="Municipalities",
        style_function=lambda x: {
            "color": "blue",
            "fillOpacity": 0.2,
            "opacity": 0.3,
        },
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m
