from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

from config.results.maps.heat_shared import (
    heat_demand_from_sources,
    residual_heat_potential,
)
from config.results.maps.gas_shared import fuel_demand, fuel_potential_and_production


class AllCarriersBalanceNormalized(AbstractResultMap):

    key = "all_carriers_balance_normalized"
    name = "Energiebalans, aanbod-vraag ratio (%)"
    unit = "%"
    colormap = ColorMapDef(
        # colormap="b_diverging_gkr_60_10_c40",
        colormap="b_diverging_bwr_55_98_c37",
        lower_limit=0,
        upper_limit=200,
        reverse=True,
    )
    legend = LegendDef(steps=9, decimals=0)
    related_carrier = CarrierEnum.ALL
    related_balance = BalanceEnum.BALANCE

    # related_area_div is optional, list or single value
    # in this case we have all but the HS/MS value
    related_area_div = [
        AreaDivisionEnum.RES,
        AreaDivisionEnum.GM,
        AreaDivisionEnum.PROV,
        AreaDivisionEnum.REG,
    ]

    @staticmethod
    def map(var: "Var"):

        # supply
        per_region_fuel_supply = fuel_potential_and_production(var)
        per_region_heat_supply = residual_heat_potential(var)
        per_region_electricity_supply = (
            var.gqueries.total_electricity_produced.future / 1e9  # MJ to PJ
        )
        total_supply = (
            per_region_fuel_supply
            + per_region_heat_supply
            + per_region_electricity_supply
        )

        # demand
        per_region_fuel_demand = fuel_demand(var)
        per_region_heat_demand = heat_demand_from_sources(var)
        per_region_electricity_demand = (
            var.gqueries.total_electricity_consumed.future / 1e9  # MJ to PJ
        )

        total_demand = (
            per_region_fuel_demand
            + per_region_heat_demand
            + per_region_electricity_demand
        )

        # Calculate balance percentage
        return total_supply / total_demand * 100

    @staticmethod
    def map_aggregate(var: "Var"):
        # supply
        per_region_fuel_supply = fuel_potential_and_production(var)
        per_region_heat_supply = residual_heat_potential(var)
        per_region_electricity_supply = (
            var.gqueries.total_electricity_produced.future / 1e9
        )  # MJ to PJ
        total_supply = (
            per_region_fuel_supply
            + per_region_heat_supply
            + per_region_electricity_supply
        )

        # demand
        per_region_fuel_demand = fuel_demand(var)
        per_region_heat_demand = heat_demand_from_sources(var)
        per_region_electricity_demand = (
            var.gqueries.total_electricity_consumed.future / 1e9
        )  # MJ to PJ

        per_region_total_demand = (
            per_region_fuel_demand
            + per_region_heat_demand
            + per_region_electricity_demand
        )

        # Calculate balance percentage
        total_balance = (
            (total_supply - per_region_total_demand) / per_region_total_demand * 100
        )

        grand_total_demand = per_region_total_demand.sum_element_wise()

        return total_balance * per_region_total_demand / grand_total_demand
