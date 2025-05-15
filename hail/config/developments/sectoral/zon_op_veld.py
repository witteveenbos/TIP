from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.sectoral._groups import grootschalige_elektriciteitsopwek

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ZonOpVeld(AbstractDevelopment):

    name = "Zon op veld"
    key = "zon_op_veld"
    unit = "MW"
    dev_type = DevelomentType.SECTORAL
    group = grootschalige_elektriciteitsopwek

    @staticmethod
    def min(var: "Var"):

        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # Neem de maximaal toegestane capaciteit uit het ETM over

        zon_op_veld = var.inputs.capacity_of_energy_power_solar_pv_solar_radiation.max

        return zon_op_veld

    @staticmethod
    def default(var: "Var"):

        zon_op_veld = (
            var.inputs.capacity_of_energy_power_solar_pv_solar_radiation.default
        )

        return zon_op_veld

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Neem de waarde van de slider uit de tool direct over in het ETM

        zon_op_veld = var.inputs.capacity_of_energy_power_solar_pv_solar_radiation

        slider = var.ui.zon_op_veld

        zon_op_veld_target = slider

        return {zon_op_veld: zon_op_veld_target}

    @classmethod
    def aggregate(cls, var: "Var"):
        solar_utility = var.ui.zon_op_veld | cls.default(var)
        return solar_utility
