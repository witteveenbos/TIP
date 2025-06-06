import geopandas as gpd

fp = [
    "data/hsms.geojson",
    "data/municipalities_simplified.geojson",
    "data/municipalities.geojson",
    "data/province_simplified.geojson",
    "data/province.geojson",
    "data/regions_simplified.geojson",
    "data/regions.geojson",
    "data/res_simplified.geojson",
    "data/res.geojson",
]

for file in fp:
    gdf = gpd.read_file(file)
    print(f"File: {file}")
    print(f"Number of geometries: {len(gdf)}")
    print(f"CRS: {gdf.crs}")
    print(f"Geometry type: {gdf.geometry.geom_type.unique()}")
    print(f"Is valid: {gdf.is_valid.all()}")
    print(f"Is simple: {gdf.is_simple.all()}")
    print("-" * 40)
    if file ==  "data/municipalities_simplified.geojson":
        print(gdf.is_valid)

# %%
gdf2 = gpd.read_file("data/base_data/geojsons_response.geojson", layer=2)
