# %%
from pathlib import Path
import yaml

from util import django_setup

# setup django so we can work with models
django_setup()


from energy.datahandler.objects import (
    ChainableUnit,
    ContinuousDevelopment,
    DerivedEnergyUnit,
    KeyEnergyFigure,
    EnergyUnitOperation,
    EnergyUnitTypes,
    OperationTypes,
    SubstitutableUnit,
    UnitChoices,
    EnergyUnitOperationBlock,
    EnergyUnitOperationCollection,
    InitialEnergyFigure,
    ScenarioEnum,
)

static = Path(__file__).parents[1] / "static" / "developments"

CONTINUOUS_FP = static / "continuous"
SECTORAL_FP = static / "sectoral"
DERIVED_FP = static / "derived"
KEYFIGURES_FP = static / "keyfigures"
INITALFIGURES_FP = static / "initialfigures"

# %% Create a sample derived energy unit
if False:  # Commented out to avoid overriding substion example
    with open(DERIVED_FP / "sample_derived_unit.yml", "w") as f:
        operations = [
            EnergyUnitOperation(
                this=EnergyUnitTypes.ELECTRICITY_SUPPLY_SOLAR_PV_BUILDINGS,
                other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                operation=OperationTypes.PRODUCT,
            ),
            EnergyUnitOperation(
                other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                operation=OperationTypes.DIVISION,
            ),
            EnergyUnitOperation(
                other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                operation=OperationTypes.PRODUCT,
            ),
        ]

        sample_derived_unit = DerivedEnergyUnit(
            operations=operations,
            name="sample_derived_unit",
        )

        yaml.dump(sample_derived_unit.model_dump(mode="json", exclude_none=True), f)

# %% Create a sample key energy figure
name = "average_electricity_production_per_mw_solar_pv_buildings"
with open(KEYFIGURES_FP / (name + ".yml"), "w") as f:
    key_energy_figure = KeyEnergyFigure(
        name=name,
        unit=UnitChoices.MWH,
        value=861,
    )

    yaml.dump(key_energy_figure.model_dump(mode="json"), f)

# %% Create a sample initial energy figure
name = "energy_saving_heating_in_households"
with open(INITALFIGURES_FP / (name + ".yml"), "w") as f:
    initial_energy_figure = InitialEnergyFigure(
        name=name,
        unit=UnitChoices.PERCENTAGE,
        value=13,
        scenario=ScenarioEnum.INTERNATIONAL_2050,
    )

    yaml.dump(initial_energy_figure.model_dump(mode="json"), f)

# %%
# %% Create a sample continous development
name = "sample_continuous_development"
with open(CONTINUOUS_FP / (name + ".yml"), "w") as f:
    continuous_development = ContinuousDevelopment(
        name=name,
        key="average_electricity_production_per_mw_solar_pv_buildings",
        min=0,
        max=100,
        default_value=861,
        unit=UnitChoices.MWH,
        mapping=DerivedEnergyUnit(
            name="sample_derived_unit",
            operations=[
                EnergyUnitOperation(
                    this=EnergyUnitTypes.ELECTRICITY_SUPPLY_SOLAR_PV_BUILDINGS,
                    other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                    operation=OperationTypes.PRODUCT,
                ),
                EnergyUnitOperation(
                    other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                    operation=OperationTypes.DIVISION,
                ),
                EnergyUnitOperation(
                    other=EnergyUnitTypes.ELECTRICITY_CURTAILMENT_SOLAR_PV_BUILDINGS,
                    operation=OperationTypes.PRODUCT,
                ),
            ],
        ),
    )

    yaml.dump(continuous_development.model_dump(mode="json"), f)
