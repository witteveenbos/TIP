import pandas as pd
from pathlib import Path
from hail.models.request import MunicipalityScenario, MainScenarioEnum
from hail.models.configuration import DistributedScenarioRelation

SOURCE = "scenario_links.xlsx"
TARGET_FOLDER = Path(__file__).parent.parent / "config" / "scenarios"

path = Path(__file__).parent / SOURCE

for i in range(10):
    try:
        df = pd.read_excel(path, sheet_name=i, header=None)
    except ValueError:
        continue

    ms = []
    for entry in df[0].to_dict().values():
        entry: str = entry
        prefix, url = entry.split(": ")
        area_code, scenario, year = prefix.split("_")
        year = "20" + year
        etm_scenario_id = url.split("/")[-1]
        ms.append(
            MunicipalityScenario(
                municipalityID=area_code, ETMscenarioID=etm_scenario_id
            )
        )

    for candidate in MainScenarioEnum._member_names_:

        if scenario in candidate and year in candidate:
            main_scenario = candidate.lower()
            break

    dsr = DistributedScenarioRelation(
        main_scenario=main_scenario,
        municipal_scenarios=ms,
    )

    # dump the model to json
    with open(TARGET_FOLDER / f"{main_scenario}.json", "w") as f:
        f.write(dsr.model_dump_json())
