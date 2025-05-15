from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import (
    efficientieverbeteringen_verspreide_industrie,
)

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

import logging

# Deze configuratie betreft alleen de Overige industrie in het ETM


class BesparingEnergievraagVerspreideIndustrie(AbstractDevelopment):

    name = "Besparing energievraag"
    key = "besparing_energievraag_verspreide_industrie"
    unit = "%"
    dev_type = DevelomentType.CONTINUOUS
    group = efficientieverbeteringen_verspreide_industrie

    @staticmethod
    def min(var: "Var"):
        # De waarde van deze schuif kan negatief zijn: dan is de industrie gegroeid
        # De minimale waarde van de schuif is daarmee begrensd
        # door de maximale groei van de industrie
        return (
            100.0
            - 1.0 * var.inputs.industry_useful_demand_for_aggregated_other_energetic.max
        )

    @staticmethod
    def max(var: "Var"):
        # Bij 100% besparing energievraag is de industrie opgeheven
        return var.Matrix(100)

    @staticmethod
    def default(var: "Var"):
        # Berekent de grootte van de industrie vergeleken met de huidige waarde (100%)
        other_industry_size_energetic = (
            var.inputs.industry_useful_demand_for_aggregated_other_energetic.user
            | var.inputs.industry_useful_demand_for_aggregated_other_energetic.default
        )

        energy_demand_reduction = 100.0 - other_industry_size_energetic

        return energy_demand_reduction

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Deze method stelt de grootte van de Overige industrie in het ETM

        other_industry_size_energetic = (
            var.inputs.industry_useful_demand_for_aggregated_other_energetic
        )

        slider = var.ui.besparing_energievraag_verspreide_industrie

        other_industry_size_energetic_target = 100.0 - slider

        return {other_industry_size_energetic: other_industry_size_energetic_target}

    @staticmethod
    def aggregate(var: "Var"):
        # Berekent een gewogen gemiddelde van de bespaarde energievraag voor de overige industrie
        # Hierbij worden de finale energievraag van de overige industrie als gewichten gebruikt

        # Bereken eerst de procentuele afname tussen de toekomstige en huidige waarde van de energievraag van Overige industrie in het ETM
        # De minimale waarde van de afname is 0 (bij gelijkblijvende of stijgende energievraag)
        other_industry_size_energetic = (
            var.inputs.industry_useful_demand_for_aggregated_other_energetic.user
        )

        energy_demand_reduction = var.max(
            100.0 - other_industry_size_energetic, var.Matrix(0)
        )

        # logging.error(f"energy_demand_reduction:{energy_demand_reduction}")

        # override the calculated value with the value from the UI, if it exists
        energy_demand_reduction = (
            var.ui.besparing_energievraag_verspreide_industrie | energy_demand_reduction
        )

        # Bereken nu de gewichten
        ## Bereken eerst finale energievraag van de overige industrie (geen bestaande query)
        final_energy_demand_other_industry = (
            var.gqueries.final_demand_of_ambient_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_biomass_products_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_coal_and_coal_gas_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_coal_and_derivatives_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_cokes_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_electricity_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_geothermal_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_heat_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_hydrogen_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_natural_gas_and_derivatives_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_oil_and_derivatives_in_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_other_non_specified_industry_energetic.present
            + var.gqueries.final_demand_of_solar_in_other_non_specified_industry_energetic.present
        )

        final_energy_demand_weights = final_energy_demand_other_industry / sum(
            final_energy_demand_other_industry
        )

        # Bereken gewogen gemiddelde
        weighted_demand_reduction = (
            final_energy_demand_weights * energy_demand_reduction
        )

        # # Geef alleen resultaat door als de gebruiker waarden gewijzigd heeft
        # weighted_demand_reduction = weighted_demand_reduction *

        return weighted_demand_reduction
