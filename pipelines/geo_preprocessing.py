import geopandas as gpd
import fiona
import matplotlib
import matplotlib.pyplot

fp_bg = "data/base_data/BestuurlijkeGebieden_2025.gpkg" #this can be downloaded from PDOK
fp_res = "data/base_data/RESregio.json" # I don't remember where i got this one...

# List available stuff
layers = fiona.listlayers(fp_bg)
print(layers)

# Usually gemeente is layer 0 and provincie is layer 2
gemeenten = gpd.read_file(fp_bg, layer=0).set_index("identificatie")
provincies = gpd.read_file(fp_bg, layer=2).set_index("identificatie")
resregio = gpd.read_file(fp_res).set_index("id")
# plotted for checks
# gemeenten.plot()
# provincies.plot()
# resregio.plot()

### Perform some cookie cutting
PROVINCIE = "Noord-Holland" 
provincie_selected = provincies[provincies["naam"] == PROVINCIE]

resregio_selected = resregio.clip(provincie_selected)
# plot to inspect that stuff, borders are weird
resregio_selected.plot(column="statnaam")

resregio_selected = resregio_selected.drop([15, 29, 6, 2])
fig, ax = matplotlib.pyplot.subplots()
resregio_selected.plot(column="statnaam", ax=ax)
provincie_selected.boundary.plot(ax=ax, facecolor=None, edgecolor="black")

gemeenten_selected = gemeenten.clip(provincie_selected)
gemeenten_selected.boundary.plot(ax=ax)





# Replace 'your_file.gpkg' with the path to your GeoPackage file

# List all layers in the GeoPackage
# %%
# fp = "data/grenzen.json"
# layers = fiona.listlayers(fp)
# print(layers)
# gdf = gpd.read_file(fp)
# gdf.plot()