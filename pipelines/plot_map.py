import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON data
with open("data/municipal_load_to_station_map.json") as f:
    data = json.load(f)

# Convert the JSON data to a pandas DataFrame


# %% Sort the DataFrame

df = pd.DataFrame(data)
df = df.T.sort_index()
sorted = []

first = True

for row, col in df.iterrows():
    # get the cols that are non-zero
    non_zero_cols = col[col > 0]
    zero_cols = col[col == 0]
    assert len(non_zero_cols) + len(zero_cols) == len(col)

    # all cols (either zero or non-zero) that are already sorted should be excluded
    non_zero_cols = non_zero_cols[~non_zero_cols.index.isin(sorted)]
    zero_cols = zero_cols[~zero_cols.index.isin(sorted)]
    assert len(non_zero_cols) + len(zero_cols) + len(sorted) == len(col)

    # move the non-zero cols to the front,
    this_row = df.loc[
        row, sorted + non_zero_cols.index.tolist() + zero_cols.index.tolist()
    ]

    sorted.extend(non_zero_cols.index.tolist())


df = df.loc[:, sorted].T


# %%
# Function to color negative values red
def custom_props(val):
    # should return bold and red if non-zero
    if val == 0:
        # should make font invisible if zero (opacity 0)
        return "color: rgba(0, 0, 0, 0)"
    else:
        return "color: red; font-weight: bold"


# Apply the cubehelix_r colormap and the custom color function
styled_df = (
    df.style.background_gradient(  # Apply custom color function
        cmap="cubehelix_r"
    )  # Apply cubehelix_r colormap
    .set_table_styles(
        [
            {"selector": "tr:hover", "props": [("background-color", "#ffff99")]},
            {"selector": "td:hover", "props": [("background-color", "#ffcccb")]},
            {
                "selector": "th.col_heading",
                "props": [("transform", "rotate(90deg)")],
            },
        ],
        overwrite=False,
    )
    .applymap(custom_props)
    .format(precision=3)  # Set precision of display to 3 decimals
)

# Save the styled DataFrame to an HTML file
styled_df.to_html("visual_checks/municipal_load_to_station_map.html")
# Display the styled DataFrame
styled_df
