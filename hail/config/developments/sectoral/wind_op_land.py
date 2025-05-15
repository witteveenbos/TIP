from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.sectoral._groups import grootschalige_elektriciteitsopwek

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class WindOpLand(AbstractDevelopment):

    name = "Wind op land"
    key = "wind_op_land"
    unit = "MW"
    dev_type = DevelomentType.SECTORAL
    group = grootschalige_elektriciteitsopwek

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # Neem de maximaal toegestane capaciteit uit het ETM over

        wind = var.inputs.capacity_of_energy_power_wind_turbine_inland.max

        return wind

    @staticmethod
    def default(var: "Var"):

        wind = var.inputs.capacity_of_energy_power_wind_turbine_inland.default

        return wind

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Neem de waarde van de slider uit de tool direct over in het ETM

        wind = var.inputs.capacity_of_energy_power_wind_turbine_inland

        slider = var.ui.wind_op_land

        wind_target = slider

        return {wind: wind_target}

    @classmethod
    def aggregate(cls, var: "Var"):
        wind_onshore = var.ui.wind_op_land | cls.default(var)
        return wind_onshore
