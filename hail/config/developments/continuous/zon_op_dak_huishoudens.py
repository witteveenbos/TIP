import logging
from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import zon_op_dak

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ZonOpDakHuishoudens(AbstractDevelopment):

    key = "zon_op_dak_huishoudens"
    name = "Huishoudens"
    unit = "MW"
    dev_type = DevelomentType.CONTINUOUS
    group = zon_op_dak

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # Neem de maximaal toegestane capaciteit uit het ETM over

        households = var.inputs.capacity_of_households_solar_pv_solar_radiation.max

        return households

    @staticmethod
    def default(var: "Var"):

        households = (
            var.inputs.capacity_of_households_solar_pv_solar_radiation.user_original
        )

        return households

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Neem de waarde van de slider uit de tool direct over in het ETM

        households = var.inputs.capacity_of_households_solar_pv_solar_radiation

        slider = var.ui.zon_op_dak_huishoudens

        household_target = slider

        return {households: household_target}

    @staticmethod
    def aggregate(var: "Var"):

        zon_op_dak_huishoudens = (
            var.ui.zon_op_dak_huishoudens
            | var.inputs.capacity_of_households_solar_pv_solar_radiation.default
        )
        return zon_op_dak_huishoudens
