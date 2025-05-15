import json
import matplotlib.pyplot as plt

# Load the JSON data
with open("hsms_capacity.json") as f:
    data = json.load(f)

# Calculate capacity and sort the data
locations = list(data.keys())
capacities = [(loc, data[loc]["invoeding"] + data[loc]["afname"]) for loc in locations]
capacities.sort(key=lambda x: x[1], reverse=True)

# Extract sorted data
sorted_locations = [item[0] for item in capacities]
sorted_invoeding = [data[loc]["invoeding"] for loc in sorted_locations]
sorted_afname = [data[loc]["afname"] for loc in sorted_locations]

# Plot the data
x = range(len(sorted_locations))

fig = plt.figure(figsize=(10, 8))  # Make the plot taller

# Plot invoeding with red markers for zero values
for i, value in enumerate(sorted_invoeding):
    if value == 0:
        plt.plot(i, value, "ro")  # red marker
    else:
        plt.plot(i, value, "bo")  # blue marker

# Plot afname with red markers for zero values
for i, value in enumerate(sorted_afname):
    if value == 0:
        plt.plot(i, value, "ro")  # red marker
    else:
        plt.plot(i, value, "go")  # green marker

plt.plot(x, sorted_invoeding, label="Invoeding", color="blue")
plt.plot(x, sorted_afname, label="Afname", color="green")
plt.xticks(x, sorted_locations, rotation="vertical")
plt.xlabel("Locations")
plt.ylabel("Values")
plt.title("Invoeding and Afname per Location (Sorted by Capacity)")
plt.legend()
plt.tight_layout()
plt.show()
# save
fig.savefig("visual_checks/hsms_capacity.png")
