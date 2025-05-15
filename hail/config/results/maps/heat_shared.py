from typing import TYPE_CHECKING

from hail.models.matrix import Matrix

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


def residual_heat_potential(var: "Var") -> Matrix:
    return (
        var.gqueries.industry_chemicals_refineries_potential_residual_heat.future
        + var.gqueries.industry_chemicals_fertilizers_potential_residual_heat.future
        + var.gqueries.industry_chemicals_other_potential_residual_heat.future
        + var.gqueries.industry_other_ict_potential_residual_heat.future
        + var.gqueries.energy_hydrogen_flexibility_p2g_potential_residual_heat.future
    )


def heat_demand_from_sources(
    var: "Var",
) -> Matrix:
    return (
        var.gqueries.final_demand_of_geothermal_energetic_in_bezier.future
        + var.gqueries.final_demand_of_heat_energetic_in_bezier.future
    )
