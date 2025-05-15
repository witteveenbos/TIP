import requests

url = "https://engine.energytransitionmodel.com/api/v3/scenarios/1271336"

body = {
    "gqueries": [
        "useful_demand_total_residences_1945_1964_bar",
        "useful_demand_total_residences_1965_1984_bar",
        "useful_demand_total_residences_1985_2004_bar",
        "useful_demand_total_residences_2005_present_bar",
        "useful_demand_total_residences_before_1945_bar",
    ]
}


r = requests.put(
    url=url,
    json=body,
)


print(r.status_code)

# %%
present = 0
future = 0
for result in r.json()["gqueries"].values():
    present += result["present"]
    future += result["future"]


print("Share is: " + str(100 * (present - future) / present) + "%")
