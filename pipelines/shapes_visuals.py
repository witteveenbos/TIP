import folium
import geopandas as gpd
import numpy as np
from itertools import product
from scipy import sparse
from owslib.wfs import WebFeatureService
import json
from shapely.prepared import prep
from shapes_mapper_grid_only import pmiek_substation_mapper


gdf_municipalities, gdf_substations = pmiek_substation_mapper()

# exclude rotterdam from the plot
gdf_municipalities: gpd.GeoDataFrame = gdf_municipalities[
    gdf_municipalities["label"] != "Rotterdam"
]
fig1 = gdf_municipalities.plot(column="invoeding", legend=True)


gdf_substations_clip: gpd.GeoDataFrame = gdf_substations.clip(
    gdf_municipalities.total_bounds
)
fig2 = gdf_substations_clip.plot(column="totaleCapaciteitInvoedingMva", legend=True)
gdf_municipalities.boundary.plot(ax=fig2, color="black")


# %%

stations: gpd.GeoDataFrame = gpd.read_file("data/hsms.geojson")
municipalities: gpd.GeoDataFrame = gpd.read_file(
    "data/municipalities_simplified.geojson"
)


m = folium.Map(location=[52.1, 5.1], zoom_start=8)

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
