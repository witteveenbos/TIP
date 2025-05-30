import geopandas as gpd
import fiona
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

######## CHECK BOTTOM OF SCRIPT FOR ACTUAL PROVINCE SPECIFIC RUN SETTINGS ##############
######## MOST PART OF THIS CODE IS GENERAL AND FOR THE ENTIRE NETHERLANDS ##############

# set filepaths 
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



# Create a for loop to establish hierarchy relations between province, resregio, and municipality

# Function to find the region with the most overlap
def find_most_overlap(geom, regions_gdf, name_col="naam"):
    max_overlap = 0
    best_match = None
    
    for idx, region in regions_gdf.iterrows():
        if geom.intersects(region.geometry):
            overlap_area = geom.intersection(region.geometry).area
            if overlap_area > max_overlap:
                max_overlap = overlap_area
                best_match = region[name_col]
    
    return best_match

# Create a dictionary to store the hierarchical relationships
hierarchy = {}

# Iterate through all municipalities
for idx, gemeente in gemeenten.iterrows():
    gemeente_name = gemeente["naam"]
    gemeente_code = gemeente["code"]
    gemeente_id = f"GM{gemeente_code.zfill(4)}"
    
    # Find which province this municipality belongs to
    province = find_most_overlap(gemeente.geometry, provincies)
    if province:
        province_obj = provincies[provincies["naam"] == province].iloc[0]
        province_id = f"PV{province_obj['code'].zfill(2)}"
        
        # Find which RES region this municipality belongs to
        res_region = find_most_overlap(gemeente.geometry, resregio, name_col="statnaam")
        if res_region:
            res_obj = resregio[resregio["statnaam"] == res_region].iloc[0]
            res_id = res_obj.name  # Using the index which is 'id'
            
            # Find the administrative region (this might be the same as RES region in some cases)
            # For simplicity, we'll use the RES region as the administrative region
            region = res_region
            region_id = f"REG{str(res_obj.name).zfill(2)}"
            
            # Store the relationships
            hierarchy[gemeente_name] = {
                "Gem_code_CBS": gemeente_code,
                "Municipality_ID": gemeente_id,
                "Region": region,
                "Region_ID": region_id,
                "RES": res_region,
                "RES_ID": res_id,
                "Provincie": province,
                "Provincie_ID": province_id
            }

# Convert the hierarchy dictionary to a DataFrame
hierarchy_df = pd.DataFrame.from_dict(hierarchy, orient='index')
hierarchy_df.reset_index(inplace=True)
hierarchy_df.rename(columns={"index": "Municipality"}, inplace=True)

# Save the hierarchy to a CSV file
hierarchy_df.to_csv("data/geo_hierarchy.csv", index=False)

print(f"Hierarchy created with {len(hierarchy_df)} municipalities")
print(f"Number of unique provinces: {hierarchy_df['Provincie'].nunique()}")
print(f"Number of unique RES regions: {hierarchy_df['RES'].nunique()}")

# Function to select a single province and plot the results
def plot_province_hierarchy(province_name):
    """
    Select a single province and plot its municipalities colored by RES region.
    
    Args:
        province_name (str): Name of the province to plot
    """
    # Filter the hierarchy DataFrame to only include municipalities in the selected province
    province_df = hierarchy_df[hierarchy_df['Provincie'] == province_name]
    
    if province_df.empty:
        print(f"No municipalities found for province: {province_name}")
        return
    
    print(f"Plotting {len(province_df)} municipalities in {province_name}")
    print(f"RES regions in {province_name}: {province_df['RES'].unique()}")
    
    # Get the province geometry
    province_geom = provincies[provincies['naam'] == province_name]
    
    if province_geom.empty:
        print(f"Province geometry not found for: {province_name}")
        return
    
    # Get the municipalities in this province
    province_municipalities = []
    for _, row in province_df.iterrows():
        muni_name = row['Municipality']
        muni_geom = gemeenten[gemeenten['naam'] == muni_name]
        if not muni_geom.empty:
            # Add the RES region to the municipality geometry for coloring
            muni_geom = muni_geom.copy()
            muni_geom['RES'] = row['RES']
            province_municipalities.append(muni_geom)
    
    if not province_municipalities:
        print(f"No municipality geometries found for province: {province_name}")
        return
    
    # Combine all municipalities into a single GeoDataFrame
    province_municipalities_gdf = pd.concat(province_municipalities)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot municipalities colored by RES region
    province_municipalities_gdf.plot(column='RES', ax=ax, legend=True, 
                                     cmap='viridis', edgecolor='black', linewidth=0.5)
    
    # Plot the province boundary
    province_geom.boundary.plot(ax=ax, color='red', linewidth=2)
    
    # Add title and labels
    ax.set_title(f'Municipalities in {province_name} by RES Region')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
    return province_df


# %% ACTUAL PROVINCIE SPECIFIC FILE GENERATION
### Select a province
PROVINCIE = "Noord-Holland" 

# Example usage:
plot_province_hierarchy(PROVINCIE)

### Perform some cookie cutting
hierarchy_df_selected = hierarchy_df[hierarchy_df['Provincie'] == PROVINCIE]
hierarchy_df_selected.to_csv("data/geo_mapping.csv", index=False)

#get the shapes
resregio_selected = resregio[resregio.index.isin(hierarchy_df_selected["RES_ID"])]

gemeenten_selected = gemeenten[gemeenten.index.isin(hierarchy_df_selected["Municipality_ID"])]

# cookie cutter for nice shape of gemeenten
# before
gemeenten_selected.plot(column="naam")
# operation
gemeenten_selected = gemeenten_selected.clip(resregio_selected)
# after
gemeenten_selected.plot(column="naam")

#saving geoshapes for geomapping script and also for the frontend shapes
# %% create a version of the municipalities with simplified geometries to reduce file size
tolerance = 10 # unit: meter - 10 meter shrinks the filesize ~10x for the gemeenten shapes
gemeenten_selected.to_file("data/municipalities.geojson")
gemeenten_selected_simplified = gemeenten_selected.copy()
gemeenten_selected_simplified["geometry"] = gemeenten_selected_simplified["geometry"].simplify(tolerance)
gemeenten_selected_simplified.to_file("data/municipalities_simplified.geojson")

resregio_selected.to_file("data/res.geojson")
resregio_selected_simplified = resregio_selected.copy()
resregio_selected_simplified["geometry"] = resregio_selected_simplified["geometry"].simplify(tolerance)
resregio_selected_simplified.to_file("data/res_simplified.geojson")

provincies_selected = provincies[provincies.index.isin(hierarchy_df_selected["Provincie_ID"])]
provincies_selected.to_file("data/province.geojson")
provincies_selected_simplified = provincies_selected.copy()
provincies_selected_simplified["geometry"] = provincies_selected_simplified["geometry"].simplify(tolerance)
provincies_selected_simplified.to_file("data/province_simplified.geojson")