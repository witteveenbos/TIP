from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import besparing_door_isolatie
from hail.models.response import InputResult

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ReductieWarmtevraag(AbstractDevelopment):

    name = "Reductie warmtevraag"
    key = "reductie_warmtevraag"
    unit = "%"
    dev_type = DevelomentType.CONTINUOUS
    group = besparing_door_isolatie

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # De maximale reductie in warmtevraag is gecapt op 70% van het heden.
        # Dit komt grofweg overeen met de maximaal beschikbare instelling in II3050 NAT (Nederland)
        return var.Matrix(70)

    @staticmethod
    def default(var: "Var"):
        # Berekent de procentuele afname tussen de toekomstige en huidige waarde van de energievraag voor ruimteverwarming in huishoudens
        # De minimale waarde van de besparing is 0 (bij gelijkblijvende of stijgende ruimteverwarmingsvraag)

        space_heating_demand_present = (
            var.gqueries.useful_demand_total_residences_1945_1964_bar.present
            + var.gqueries.useful_demand_total_residences_1965_1984_bar.present
            + var.gqueries.useful_demand_total_residences_1985_2004_bar.present
            + var.gqueries.useful_demand_total_residences_2005_present_bar.present
            + var.gqueries.useful_demand_total_residences_before_1945_bar.present
        )

        space_heating_demand_future = (
            var.gqueries.useful_demand_total_residences_1945_1964_bar.future
            + var.gqueries.useful_demand_total_residences_1965_1984_bar.future
            + var.gqueries.useful_demand_total_residences_1985_2004_bar.future
            + var.gqueries.useful_demand_total_residences_2005_present_bar.future
            + var.gqueries.useful_demand_total_residences_before_1945_bar.future
        )

        demand_reduction = var.max(
            100.0
            * (space_heating_demand_present - space_heating_demand_future)
            / space_heating_demand_present,
            var.Matrix(0),
        )

        return demand_reduction

    @staticmethod
    def sets_ETM_value(var: "Var"):
        slider = var.ui.reductie_warmtevraag
        reduction_factor = (100.0 - slider) / 100.0

        def determine_target_value(input_el: InputResult):
            current_value = input_el.default
            min_value = input_el.min
            target_value = var.max(current_value * reduction_factor, min_value)
            masked_target_value = target_value * slider.mask
            return masked_target_value

        input_elements = [
            var.inputs.households_insulation_level_apartments_1945_1964,
            var.inputs.households_insulation_level_apartments_1965_1984,
            var.inputs.households_insulation_level_apartments_1985_2004,
            var.inputs.households_insulation_level_apartments_2005_present,
            var.inputs.households_insulation_level_apartments_before_1945,
            var.inputs.households_insulation_level_detached_houses_1945_1964,
            var.inputs.households_insulation_level_detached_houses_1965_1984,
            var.inputs.households_insulation_level_detached_houses_1985_2004,
            var.inputs.households_insulation_level_detached_houses_2005_present,
            var.inputs.households_insulation_level_detached_houses_before_1945,
            var.inputs.households_insulation_level_semi_detached_houses_1945_1964,
            var.inputs.households_insulation_level_semi_detached_houses_1965_1984,
            var.inputs.households_insulation_level_semi_detached_houses_1985_2004,
            var.inputs.households_insulation_level_semi_detached_houses_2005_present,
            var.inputs.households_insulation_level_semi_detached_houses_before_1945,
            var.inputs.households_insulation_level_terraced_houses_1945_1964,
            var.inputs.households_insulation_level_terraced_houses_1965_1984,
            var.inputs.households_insulation_level_terraced_houses_1985_2004,
            var.inputs.households_insulation_level_terraced_houses_2005_present,
            var.inputs.households_insulation_level_terraced_houses_before_1945,
        ]
        return {
            input_el: determine_target_value(input_el) for input_el in input_elements
        }

    @staticmethod
    def aggregate(var: "Var"):
        # Berekent een gewogen gemiddelde van de bespaarde energievraag voor ruimteverwarming in huishoudens
        # Hierbij wordt de finale warmtevraag voor ruimteverwarming in de huidige situatie als gewicht genomen

        # Bereken eerst de procentuele afname tussen de toekomstige en huidige waarde van de energievraag voor ruimteverwarming in huishoudens
        # De minimale waarde van de besparing is 0 (bij gelijkblijvende of stijgende ruimteverwarmingsvraag)

        # CORRECTIE: verander demand_reduction deel door de nieuwe default functie
        space_heating_demand_present = (
            var.gqueries.useful_demand_total_residences_1945_1964_bar.present
            + var.gqueries.useful_demand_total_residences_1965_1984_bar.present
            + var.gqueries.useful_demand_total_residences_1985_2004_bar.present
            + var.gqueries.useful_demand_total_residences_2005_present_bar.present
            + var.gqueries.useful_demand_total_residences_before_1945_bar.present
        )

        space_heating_demand_future = (
            var.gqueries.useful_demand_total_residences_1945_1964_bar.future
            + var.gqueries.useful_demand_total_residences_1965_1984_bar.future
            + var.gqueries.useful_demand_total_residences_1985_2004_bar.future
            + var.gqueries.useful_demand_total_residences_2005_present_bar.future
            + var.gqueries.useful_demand_total_residences_before_1945_bar.future
        )

        demand_reduction = var.max(
            -1.0
            * (space_heating_demand_future - space_heating_demand_present)
            / space_heating_demand_present,
            var.Matrix(0),
        )

        # Bereken nu de gewichten
        space_heating_demand_weights = space_heating_demand_present / sum(
            space_heating_demand_present
        )

        # Bereken gewogen gemiddelden
        weighted_demand_reduction = space_heating_demand_weights * demand_reduction

        return weighted_demand_reduction
