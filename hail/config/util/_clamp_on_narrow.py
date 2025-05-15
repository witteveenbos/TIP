from typing import Literal
from hail.models.matrix import Matrix
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


def clamp_on_narrow(var: "Var", on: Literal["upper", "lower"]):
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
    def final_future_demand(
        carrier: Literal["heat", "electricity"],
        min_max: Literal["upper", "lower"],
        max_change_factor: float = 0.95,
    ) -> Matrix:

        if carrier == "heat":
            demand = heat_demand_present
            useful_demand = var.inputs.agriculture_useful_demand_useable_heat
            energy_density = energy_density_greenhouses_heat
        elif carrier == "electricity":
            demand = electricity_demand_present
            useful_demand = var.inputs.agriculture_useful_demand_electricity
            energy_density = energy_density_greenhouses_electricity

        annual_change_percentage = (
            max_change_factor * useful_demand.min
            if on == "lower"
            else max_change_factor * useful_demand.max
        )

        annual_change_factor = annual_change_percentage / 100 + 1

        total_change_factor = pow(annual_change_factor, scenario_duration)

        final_demand = demand * total_change_factor

        return final_demand / energy_density

    min_surface_area_electricity = final_future_demand("electricity", on="lower")
    max_surface_area_electricity = final_future_demand("electricity", on="upper")
    min_surface_area_heat = final_future_demand("heat", on="lower")
    max_surface_area_heat = final_future_demand("heat", on="upper")

    # TODO: now determine the minimal absolute value and use that for the clamp
