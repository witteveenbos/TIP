from typing import TYPE_CHECKING

from hail.models.matrix import Matrix

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


def fuel_demand(var: "Var") -> Matrix:
    return (
        var.gqueries.final_demand_of_biomass_products_energetic_in_bezier.future
        + var.gqueries.final_demand_of_natural_gas_and_derivatives_energetic_in_bezier.future
        + var.gqueries.final_demand_of_hydrogen_energetic_in_bezier.future
    )


def fuel_potential_and_production(
    var: "Var",
) -> Matrix:
    return (
        var.gqueries.max_demand_biogenic_waste.future
        + var.gqueries.max_demand_wet_biomass.future
        + var.gqueries.max_demand_dry_biomass.future
        + var.gqueries.max_demand_oily_biomass.future
        + var.gqueries.energy_hydrogen_flexibility_p2g_electricity_for_mekko.future
        + var.gqueries.energy_hydrogen_electrolysis_wind_electricity_for_mekko.future
        + var.gqueries.energy_hydrogen_hybrid_electrolysis_wind_electricity_for_mekko.future
        + var.gqueries.energy_hydrogen_biomass_gasification_ccs_for_mekko.future
        + var.gqueries.energy_hydrogen_biomass_gasification_for_mekko.future
        + var.gqueries.energy_hydrogen_electrolysis_solar_electricity_for_mekko.future
        + var.gqueries.energy_hydrogen_steam_methane_reformer_must_run_for_mekko.future
        + var.gqueries.energy_hydrogen_steam_methane_reformer_ccs_must_run_for_mekko.future
        + var.gqueries.energy_hydrogen_steam_methane_reformer_dispatchable_for_mekko.future
        + var.gqueries.energy_hydrogen_autothermal_reformer_must_run_for_mekko.future
        + var.gqueries.energy_hydrogen_autothermal_reformer_ccs_must_run_for_mekko.future
        + var.gqueries.energy_hydrogen_autothermal_reformer_dispatchable_for_mekko.future
        + var.gqueries.energy_hydrogen_ammonia_reformer_must_run_for_mekko.future
        + var.gqueries.energy_hydrogen_ammonia_reformer_dispatchable_for_mekko.future
        + var.gqueries.hydrogen_supply_transformation_chemical_fertilizers_industry.future
        + var.gqueries.hydrogen_supply_transformation_chemical_other_industry.future
        + var.gqueries.hydrogen_supply_transformation_chemical_refineries_industry.future
    )
