from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import verduurzaming_utiliteiten
from config.developments.shared import set_heat_sliders_buildings

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

    # All-electric omvat luchtwarmtepomp, bodemwarmtepomp, TEO-warmtepomp en elektrische ketel


class AllElectricUtiliteiten(AbstractDevelopment):

    name = "All-electric"
    key = "utiliteiten_all_electric"
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
        # Deze method berekent handmatig het aantal bestaande utiliteiten op een all-electric oplossing
        # Hier bestaan (vooralsnog) geen voorgedefinieerde queries voor in het ETM
        # Dit werkt zolang er geen nieuwbouwutiliteiten in de tool bijgeplaatst kunnen worden

        number_of_buildings = var.inputs.buildings_number_of_buildings_present.default

        hp_air_share = (
            var.inputs.buildings_space_heater_heatpump_air_water_electricity_share.default
        )
        hp_ground_share = (
            var.inputs.buildings_space_heater_collective_heatpump_water_water_ts_electricity_share.default
        )
        hp_aquathermal_share = (
            var.inputs.buildings_space_heater_heatpump_surface_water_water_ts_electricity_share.default
        )
        electric_heater_share = (
            var.inputs.buildings_space_heater_electricity_share.default
        )

        total_electric_share = (
            hp_air_share
            + hp_ground_share
            + hp_aquathermal_share
            + electric_heater_share
        ) / 100

        number_of_buildings_all_electric = total_electric_share * number_of_buildings

        return number_of_buildings_all_electric

    @staticmethod
    def sets_ETM_value(var: "Var"):
        return set_heat_sliders_buildings(var)

    @classmethod
    def aggregate(cls, var: "Var"):
        return var.ui.utiliteiten_all_electric | cls.default(var)
