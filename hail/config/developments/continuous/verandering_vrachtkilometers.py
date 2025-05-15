from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import energie_nodig_vrachtvervoer

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class VeranderingVrachtkilometers(AbstractDevelopment):

    name = "Verandering vrachtkilometers"
    key = "verandering_vrachtkilometers"
    unit = "%"
    dev_type = DevelomentType.CONTINUOUS
    group = energie_nodig_vrachtvervoer

    @staticmethod
    def min(var: "Var"):
        # De laagst mogelijke waarde van totale procentuele verandering in vrachtkilometers is begrensd
        # door de minimale waarde van de jaarlijkse verandering in vrachtkilometers
        scenario_duration = var.gqueries.scenario_duration.future
        annual_change_percentage = (
            var.inputs.transport_useful_demand_freight_tonne_kms.min
        )

        annual_change_factor = 1.0 + annual_change_percentage / 100.0

        total_change_factor = pow(annual_change_factor, scenario_duration)

        total_change_percentage = 0.95 * (total_change_factor - 1.0) * 100.0

        return total_change_percentage

    @staticmethod
    def max(var: "Var"):
        # De hoogst mogelijke waarde van totale procentuele verandering in vrachtkilometers is begrensd
        # door de maximale waarde van de jaarlijkse verandering in vrachtkilometers
        scenario_duration = var.gqueries.scenario_duration.future
        annual_change_percentage = (
            var.inputs.transport_useful_demand_freight_tonne_kms.max
        )

        annual_change_factor = 1.0 + annual_change_percentage / 100.0

        total_change_factor = pow(annual_change_factor, scenario_duration)

        total_change_percentage = 0.95 * (total_change_factor - 1.0) * 100.0

        return total_change_percentage

    @staticmethod
    def default(var: "Var"):
        # Reken de jaarlijkse verandering uit het ETM om naar totale verandering voor de duur van het scenario

        scenario_duration = var.gqueries.scenario_duration.future
        annual_change_percentage = (
            var.inputs.transport_useful_demand_freight_tonne_kms.user_original
        )

        annual_change_factor = 1.0 + annual_change_percentage / 100.0

        total_change_factor = pow(annual_change_factor, scenario_duration)

        total_change_percentage = (total_change_factor - 1.0) * 100.0

        return total_change_percentage

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Reken de ingevoerde totale verandering uit de tool om naar jaarlijkse verandering voor het ETM

        scenario_duration = var.gqueries.scenario_duration.future
        annual_change_percentage = var.inputs.transport_useful_demand_freight_tonne_kms

        slider = var.ui.verandering_vrachtkilometers

        total_change_factor = (slider / 100.0) + 1.0
        annual_change_factor = pow(total_change_factor, 1.0 / scenario_duration)

        annual_change_percentage_target = (annual_change_factor - 1.0) * 100.0

        return {annual_change_percentage: annual_change_percentage_target}

    @staticmethod
    def aggregate(var: "Var"):
        # Berekent een gewogen gemiddelde van de verandering in vrachtkilometers
        # Hierbij wordt de finale energievraag voor vrachttransport in de huidige situatie als gewicht genomen

        # Reken de jaarlijkse verandering uit het ETM om naar totale verandering voor de duur van het scenario
        scenario_duration = var.gqueries.scenario_duration.future
        annual_change_percentage = (
            var.inputs.transport_useful_demand_freight_tonne_kms.user
        )

        annual_change_factor = 1.0 + annual_change_percentage / 100.0

        total_change_factor = pow(annual_change_factor, scenario_duration)

        total_change_percentage = (total_change_factor - 1.0) * 100.0

        # override the calculated value with the value from the UI, if it exists
        total_change_percentage = (
            var.ui.verandering_vrachtkilometers | total_change_percentage
        )

        # Bereken de gewichten
        final_demand_freight_transport_present = (
            var.gqueries.final_demand_freight_transport.present
        )
        final_demand_freight_transport_weights = (
            final_demand_freight_transport_present
            / sum(final_demand_freight_transport_present)
        )

        # Bereken gewogen gemiddelde
        freight_km_weighted = (
            final_demand_freight_transport_weights * total_change_percentage
        )

        return freight_km_weighted
