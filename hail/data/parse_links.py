import pandas as pd
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hail.models.request import MunicipalityScenario, MainScenarioEnum
from hail.models.configuration import DistributedScenarioRelation

SOURCE = "scenario_links.xlsx"
TARGET_FOLDER = Path(__file__).parent.parent / "config" / "scenarios"

path = Path(__file__).parent / SOURCE

excel_file = pd.ExcelFile(path)

for sheet_name in excel_file.sheet_names:
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    except ValueError:
        continue
    
    ms = []
    for idx, row in df.iterrows():
        area_code = row[0]
        url:str = row[1]
        scenario = sheet_name.split(" ")[0]
        year = sheet_name.split(" ")[-1]
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
