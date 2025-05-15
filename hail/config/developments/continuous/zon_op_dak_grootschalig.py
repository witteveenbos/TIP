from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import zon_op_dak

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ZonOpDakGrootschalig(AbstractDevelopment):

    key = "zon_op_dak_grootschalig"
    name = "Utiliteiten"
    unit = "MW"
    dev_type = DevelomentType.CONTINUOUS
    group = zon_op_dak

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # Neem de maximaal toegestane capaciteit uit het ETM over

        buildings = var.inputs.capacity_of_buildings_solar_pv_solar_radiation.max

        return buildings

    @staticmethod
    def default(var: "Var"):

        buildings = (
            var.inputs.capacity_of_buildings_solar_pv_solar_radiation.user_original
        )

        return buildings

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Neem de waarde van de slider uit de tool direct over in het ETM

        buildings = var.inputs.capacity_of_buildings_solar_pv_solar_radiation

        slider = var.ui.zon_op_dak_grootschalig

        buildings_target = slider

        return {buildings: buildings_target}

    @staticmethod
    def aggregate(var: "Var"):

        zon_op_dak = (
            var.ui.zon_op_dak_grootschalig
            | var.inputs.capacity_of_buildings_solar_pv_solar_radiation.default
        )

        return zon_op_dak
