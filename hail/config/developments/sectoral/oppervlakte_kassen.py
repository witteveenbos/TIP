from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.sectoral._groups import uitbreiding_glastuinbouw

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class OppervlakteKassen(AbstractDevelopment):

    name = "Oppervlakte kassen"
    key = "oppervlakte_kassen"
    unit = "ha"
    dev_type = DevelomentType.SECTORAL
    group = uitbreiding_glastuinbouw

    @staticmethod
    def min(var: "Var"):
        # De maximale waarde van de finale vraag is begrensd door de maximale jaarlijkse krimp van de nuttige elektriciteits- of warmtevraag
        # Deze method schat daarom de minimale finale vraag uit adhv de maximale jaarlijkse krimp van de nuttige elektriciteits- en warmtevraag
        # en rekent dit om naar een minimale kasoppervlakte voor elektriciteit en warmte via kentallen voor energiedichtheid.
        # De hoogste berekende kasoppervlakte is uiteindelijk bepalend.

        # Definieer kentallen voor energiedichtheid van kassen
        energy_density_greenhouses_electricity = (
            0.00423  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )
        energy_density_greenhouses_heat = (
            0.00567  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )

        ## 1. Haal relevante waarden uit ETM op
        electricity_demand_present = (
            var.gqueries.final_demand_of_electricity_in_agriculture.present
        )
        heat_demand_present = var.gqueries.final_demand_of_heat_in_agriculture.present
        scenario_duration = var.gqueries.scenario_duration.future

        # 2. Begrens minimale jaarlijkse veranderpercentages op 95% van ETM-maximum
        max_change_factor = 0.95
        annual_change_electricity_percentage = max_change_factor * (
            var.inputs.agriculture_useful_demand_electricity.min
        )
        annual_change_heat_percentage = max_change_factor * (
            var.inputs.agriculture_useful_demand_useable_heat.min
        )

        # 3. Reken de minimale toegestane finale vraag uit
        ## Eerst elektriciteit
        ### Bereken groeifactor over duur van scenario
        annual_change_electricity_factor = (
            annual_change_electricity_percentage / 100 + 1
        )

        total_change_electricity_factor = pow(
            annual_change_electricity_factor, scenario_duration
        )

        ### Bereken de minimaal toegestane elektriciteitsvraag en daarmee het maximaal toegestane oppervlakte o.b.v. elektriciteit
        min_electricity_demand = (
            electricity_demand_present * total_change_electricity_factor
        )
        surface_area_electricity = (
            min_electricity_demand / energy_density_greenhouses_electricity
        )

        # logging.info(f"Min surface_area_electricity = {surface_area_electricity}")

        ## Nu warmte
        ### Groeifactor voor duur van scenario
        annual_change_heat_factor = annual_change_heat_percentage / 100 + 1

        total_change_heat_factor = pow(annual_change_heat_factor, scenario_duration)

        ### Bereken maximale toegestane warmtevraag en daarmee de maximaal toegestane oppervlakte o.b.v. warmte
        min_heat_demand = heat_demand_present * total_change_heat_factor
        surface_area_heat = min_heat_demand / energy_density_greenhouses_heat

        # 4. Minimaal toegestane oppervlakte is de hoogste van warmte of elektriciteit
        # tenzij één van beide 0 is, dan 0 (anders kan min hoger zijn dan max)
        min_surface_area = var.max(surface_area_electricity, surface_area_heat)
        min_surface_area = (surface_area_electricity == 0).mask * var.Matrix(
            0
        ) | min_surface_area
        min_surface_area = (surface_area_heat == 0).mask * var.Matrix(
            0
        ) | min_surface_area

        return min_surface_area

    @staticmethod
    def max(var: "Var"):
        # De maximale waarde van de finale vraag is begrensd door de maximale jaarlijkse groei van de nuttige elektriciteits- of warmtevraag
        # Deze method schat daarom de maximale finale vraag uit adhv de maximale jaarlijkse groei van de nuttige elektriciteits- en warmtevraag
        # en rekent dit om naar een maximale kasoppervlakte voor elektriciteit en warmte via kentallen voor energiedichtheid.
        # De laagste berekende kasoppervlakte is uiteindelijk bepalend.

        # Definieer kentallen voor energiedichtheid van kassen
        energy_density_greenhouses_electricity = (
            0.00423  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )
        energy_density_greenhouses_heat = (
            0.00567  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )

        ## 1. Haal relevante waarden uit ETM op
        electricity_demand_present = (
            var.gqueries.final_demand_of_electricity_in_agriculture.present
        )
        heat_demand_present = var.gqueries.final_demand_of_heat_in_agriculture.present
        scenario_duration = var.gqueries.scenario_duration.future

        # 2. Begrens maximale jaarlijkse veranderpercentages op 95% van ETM-maximum
        max_change_factor = 0.95
        annual_change_electricity_percentage = max_change_factor * (
            var.inputs.agriculture_useful_demand_electricity.max
        )
        annual_change_heat_percentage = max_change_factor * (
            var.inputs.agriculture_useful_demand_useable_heat.max
        )

        # 3. Reken de maximale toegestane finale vraag uit
        ## Eerst elektriciteit
        ### Bereken groeifactor over duur van scenario
        annual_change_electricity_factor = (
            annual_change_electricity_percentage / 100 + 1
        )

        total_change_electricity_factor = pow(
            annual_change_electricity_factor, scenario_duration
        )

        ### Bereken de maximaal toegestane elektriciteitsvraag en daarmee het maximaal toegestane oppervlakte o.b.v. elektriciteit
        max_electricity_demand = (
            electricity_demand_present * total_change_electricity_factor
        )
        surface_area_electricity = (
            max_electricity_demand / energy_density_greenhouses_electricity
        )

        # logging.info(f"Max surface_area_electricity = {surface_area_electricity}")

        ## Nu warmte
        ### Groeifactor voor duur van scenario
        annual_change_heat_factor = annual_change_heat_percentage / 100 + 1

        total_change_heat_factor = pow(annual_change_heat_factor, scenario_duration)

        ### Bereken maximale toegestane warmtevraag en daarmee de maximaal toegestane oppervlakte o.b.v. warmte
        max_heat_demand = heat_demand_present * total_change_heat_factor
        surface_area_heat = max_heat_demand / energy_density_greenhouses_heat

        # logging.info(f"Max surface_area_heat = {surface_area_heat}")

        # 4. Maximaal toegestane oppervlakte is de laagste van warmte of elektriciteit
        max_surface_area = var.min(surface_area_electricity, surface_area_heat)

        # logging.info(f"Max surface_area_TOTAL = {max_surface_area}")

        return max_surface_area

    @staticmethod
    def default(var: "Var"):
        energy_density_greenhouses_electricity = (
            0.00423  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )

        electricity_demand = (
            var.gqueries.final_demand_of_electricity_in_agriculture.future
        )

        surface_area_electricity = (
            electricity_demand / energy_density_greenhouses_electricity
        )

        return surface_area_electricity

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Deze method berekent de relatieve verandering in kasoppervlakte van de ingevoerde waarde uit de tool
        # ten opzichte van de berekende waarde op basis van het ETM
        # Deze relatieve verandering wordt vervolgens gebruikt om de jaarlijkse relatieve verandering in nuttige warmte- of elektriciteitsvraag te berekenen

        energy_density_greenhouses_electricity = (
            0.00423  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )
        energy_density_greenhouses_heat = (
            0.00567  # in PJ/ha, gebaseerd op CBS en ETM (2019)
        )

        # Haal relevante waarden uit ETM op
        scenario_duration = var.gqueries.scenario_duration.future
        electricity_demand_present = (
            var.gqueries.final_demand_of_electricity_in_agriculture.present
        )
        heat_demand_present = var.gqueries.final_demand_of_heat_in_agriculture.present

        # Haal sliders als object op
        annual_change_useful_demand_electricity_percentage = (
            var.inputs.agriculture_useful_demand_electricity
        )
        annual_change_useful_demand_heat_percentage = (
            var.inputs.agriculture_useful_demand_useable_heat
        )

        # Bereken huidige kasoppervlakte op basis van huidige (bijv 2019) energievraag
        surface_area_electricity = (
            electricity_demand_present / energy_density_greenhouses_electricity
        )
        surface_area_heat = heat_demand_present / energy_density_greenhouses_heat

        # Haal relevante waarde uit de tool op
        slider = var.ui.oppervlakte_kassen

        # Bereken jaarlijkse veranderpercentage op basis van verandering in kasoppervlakte
        ## Eerst elektriciteit
        total_change_surface_area_factor_electricity = slider / surface_area_electricity

        # Check: klopt de syntax in de regels hieronder?
        annual_change_surface_area_factor_electricity = pow(
            total_change_surface_area_factor_electricity, 1.0 / scenario_duration
        )

        annual_change_surface_area_percentage_electricity = (
            annual_change_surface_area_factor_electricity - 1.0
        ) * 100.0

        # Stel jaarlijkse verandering in nuttige warmtevraag gelijk aan berekende jaarlijkse veranderpercentage van de oppervlaktes
        annual_change_useful_demand_electricity_percentage_target = (
            annual_change_surface_area_percentage_electricity
        )

        ## Nu warmte
        total_change_surface_area_factor_heat = slider / surface_area_heat

        annual_change_surface_area_factor_heat = pow(
            total_change_surface_area_factor_heat, 1.0 / scenario_duration
        )

        annual_change_surface_area_percentage_heat = (
            annual_change_surface_area_factor_heat - 1.0
        ) * 100.0

        annual_change_useful_demand_heat_percentage_target = (
            annual_change_surface_area_percentage_heat
        )

        return {
            annual_change_useful_demand_electricity_percentage: annual_change_useful_demand_electricity_percentage_target,
            annual_change_useful_demand_heat_percentage: annual_change_useful_demand_heat_percentage_target,
        }

    @classmethod
    def aggregate(cls, var: "Var"):
        area = var.ui.oppervlakte_kassen | cls.default(var)
        return area
