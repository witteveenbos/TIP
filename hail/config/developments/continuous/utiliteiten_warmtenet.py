from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import verduurzaming_utiliteiten
from config.developments.shared import set_heat_sliders_buildings

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class WarmtenetUtiliteiten(AbstractDevelopment):

    name = "Warmtenet"
    key = "utiliteiten_warmtenet"
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

        heat_network_ht_share = (
            var.inputs.buildings_space_heater_district_heating_ht_steam_hot_water_share.user_original
        )
        heat_network_mt_share = (
            var.inputs.buildings_space_heater_district_heating_mt_steam_hot_water_share.user_original
        )
        heat_network_lt_share = (
            var.inputs.buildings_space_heater_district_heating_lt_steam_hot_water_share.user_original
        )

        total_heat_network_share = (
            heat_network_ht_share + heat_network_mt_share + heat_network_lt_share
        ) / 100

        number_of_buildings_heat_network = (
            number_of_buildings * total_heat_network_share
        )

        return number_of_buildings_heat_network

    @staticmethod
    def sets_ETM_value(var: "Var"):
        return set_heat_sliders_buildings(var)

    @classmethod
    def aggregate(cls, var: "Var"):
        return var.ui.utiliteiten_warmtenet | cls.default(var)
