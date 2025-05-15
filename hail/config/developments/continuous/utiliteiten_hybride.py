from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import verduurzaming_utiliteiten
from config.developments.shared import set_heat_sliders_buildings

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class HybrideUtiliteiten(AbstractDevelopment):

    name = "Hybride"
    key = "utiliteiten_hybride"
    unit = "#"
    dev_type = DevelomentType.CONTINUOUS
    group = verduurzaming_utiliteiten

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # Stel maximaal de bestaande gebouwvoorraad in op een warmteoplossing

        number_of_buildings = var.inputs.buildings_number_of_buildings_present.max

        return number_of_buildings

    @staticmethod
    def default(var: "Var"):

        number_of_buildings = var.gqueries.number_of_buildings_present.future

        hybrid_hp_network_gas_share = (
            var.inputs.buildings_space_heater_hybrid_heatpump_air_water_electricity_share.default
        )
        hybrid_hp_hydrogen_share = (
            var.inputs.buildings_space_heater_hybrid_hydrogen_heatpump_air_water_electricity_share.default
        )

        total_hybrid_hp_share = (
            hybrid_hp_network_gas_share + hybrid_hp_hydrogen_share
        ) / 100

        number_of_buildings_hybrid_hp = number_of_buildings * total_hybrid_hp_share

        return number_of_buildings_hybrid_hp

    @staticmethod
    def sets_ETM_value(var: "Var"):
        return set_heat_sliders_buildings(var)

    @classmethod
    def aggregate(cls, var: "Var"):
        return var.ui.utiliteiten_hybride | cls.default(var)
