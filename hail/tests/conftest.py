import json
from pathlib import Path
import pytest

from hail.development import AbstractDevelopment
from hail.generate import import_all_classes_from_folder
from hail.models.request import (
    MunicipalityScenario,
    PostUserInputRequest,
    SectoralDevPerMunicipality,
    UpdatedMunicipalityScenario,
    ContinuousDevPerMunicipality,
    UpdatedInput,
    UserSettings,
    ViewSettings,
)
from hail.models.enums import (
    AreaDivisionEnum,
    BalanceEnum,
    CarrierEnum,
    DevelomentType,
    MainScenarioEnum,
    MunicipalityIDs,
)
from hail.reference.maps import MapTypes

from hail.models.state import PreloadedState
from hail.parse import find_all_accessed_attributes

CONFIG = Path(__file__).parent.parent / "config"


@pytest.fixture
def request_with_changes() -> PostUserInputRequest:
    request = PostUserInputRequest(
        viewSettings=ViewSettings(
            energyCarrier=CarrierEnum.ELECTRICITY,
            balance=BalanceEnum.BALANCE,
            original=False,
            developmentType=DevelomentType.CONTINUOUS,
            areaDivision=AreaDivisionEnum.GM,
            mapType=MapTypes.ELECTRICITY_BALANCE_NORMALIZED,
            graphType=None,
        ),
        userSettings=UserSettings(
            selectedScenario=MainScenarioEnum.II3050_DEC_NL2019_CY2012_2040,
            municipalityScenarios=[
                UpdatedMunicipalityScenario(
                    ETMscenarioID=1, municipalityID=MunicipalityIDs.GM0518.name
                ),
                UpdatedMunicipalityScenario(
                    ETMscenarioID=2, municipalityID=MunicipalityIDs.GM0513.name
                ),
            ],
            continuousDevelopments=[
                ContinuousDevPerMunicipality(
                    municipalityID=MunicipalityIDs.GM0518.name,
                    devGroupKey="zon_op_dak",
                    changes=[UpdatedInput(devKey="zon_op_dak_huishoudens", value=10.0)],
                )
            ],
            sectoralDevelopments=[
                SectoralDevPerMunicipality(
                    projectName="project1",
                    projectId="1111",
                    municipalityID=MunicipalityIDs.GM0513.name,
                    devGroupKey="nieuwbouwprojecten",
                    changes=[UpdatedInput(devKey="all_electric", value=11.1)],
                ),
                SectoralDevPerMunicipality(
                    projectName="project2",
                    projectId="2222",
                    municipalityID=MunicipalityIDs.GM0513.name,
                    devGroupKey="nieuwbouwprojecten",
                    changes=[UpdatedInput(devKey="all_electric", value=22.2)],
                ),
            ],
        ),
    )

    return request


@pytest.fixture
def preloaded_state():
    preloaded = PreloadedState()
    preloaded.accessed_attributes = find_all_accessed_attributes(CONFIG)
    preloaded.developmentclasses = import_all_classes_from_folder(
        CONFIG, AbstractDevelopment
    )
    return preloaded


@pytest.fixture
def request_without_changes():
    with open(Path(__file__).parent / "fixtures" / "example_scenarios.json") as f:
        example_scenarios = json.load(f)
    return PostUserInputRequest(
        userSettings=UserSettings(
            selectedScenario=MainScenarioEnum.II3050_DEC_NL2019_CY2012_2040,
            municipalityScenarios=[
                MunicipalityScenario(
                    municipalityID=scenario["municipalityID"],
                    ETMscenarioID=scenario["ETMscenarioID"],
                )
                for scenario in example_scenarios
            ],
        ),
        viewSettings=ViewSettings(
            energyCarrier=CarrierEnum.ELECTRICITY,
            balance=BalanceEnum.BALANCE,
            original=False,
            developmentType=DevelomentType.CONTINUOUS,
            areaDivision=AreaDivisionEnum.GM,
            mapType=MapTypes.ELECTRICITY_BALANCE_NORMALIZED,
            graphType=None,
        ),
    )
