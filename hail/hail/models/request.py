from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from hail.models.enums import (
    AreaDivisionEnum,
    AllAreaDivisionIDs,
    BalanceEnum,
    CarrierEnum,
    DevelomentType,
    MunicipalityIDs,
    MainScenarioEnum,
)
from hail.reference.graphs import GraphTypes


### For get_develoment_list (e.g. initial layout render)
class MunicipalityScenario(BaseModel):
    ETMscenarioID: int
    municipalityID: MunicipalityIDs


### For put_user_values (e.g. interface for any calculations with user input)
# TODO: this implementation is to match the frontend, but it should be regarded as technical debt
class UpdatedMunicipalityScenario(MunicipalityScenario):
    # explicit that these are the scenarios that should be updated
    pass


class UpdatedInput(BaseModel):
    devKey: str
    value: float | int


class DevelopmentPerMunicipality(BaseModel):
    municipalityID: MunicipalityIDs
    devGroupKey: str
    changes: list[UpdatedInput]


class ContinuousDevPerMunicipality(DevelopmentPerMunicipality):
    pass


class SectoralDevPerMunicipality(DevelopmentPerMunicipality):
    projectName: str
    projectId: str
    isDefault: Optional[bool] = None


class UserSettings(BaseModel):
    municipalityScenarios: list[UpdatedMunicipalityScenario | MunicipalityScenario]
    # ^^ TODO: to match the residuals of a split initial/consequential, but it should be regarded as technical debt
    selectedScenario: MainScenarioEnum
    continuousDevelopments: Optional[list[ContinuousDevPerMunicipality]] = None
    sectoralDevelopments: Optional[list[SectoralDevPerMunicipality]] = None


class ViewSettings(BaseModel):
    areaDivision: AreaDivisionEnum
    energyCarrier: CarrierEnum
    balance: BalanceEnum
    original: bool
    developmentType: DevelomentType
    areaDivision: AreaDivisionEnum
    graphType: Optional[GraphTypes] = None
    graphFocus: Optional[AllAreaDivisionIDs] = None


class PostUserInputRequest(BaseModel):
    viewSettings: ViewSettings
    userSettings: Optional[UserSettings] = None


class CreateScenariosRequest(BaseModel):
    dataLink: MainScenarioEnum
