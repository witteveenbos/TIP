import json
from pathlib import Path
from hail.models.enums import MainScenarioEnum
from pydantic import BaseModel
from typing import Optional


class ScenarioDisplay(BaseModel):
    dataLink: MainScenarioEnum
    title: str
    description: str

    @staticmethod
    def multiple_from_config(config_folder_path: Path):
        with open(config_folder_path / "scenarios" / "scenario-list.json") as f:
            try:
                data = json.load(f)
                return [ScenarioDisplay(**obj) for obj in data]
            except:
                raise ValueError(
                    "Could not find a valid scenario-list.json file in 'config/scenarios/' (obj: hail.models.scenario.ScenarioDisplay) "
                )
