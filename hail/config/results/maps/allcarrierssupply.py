from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

from config.results.maps.heat_shared import (
    residual_heat_potential,
)
from config.results.maps.gas_shared import fuel_potential_and_production


class AllCarriersSupplyAbsolute(AbstractResultMap):

    key = "all_carriers_supply"
    name = "Totale energieproductie"
    unit = "PJ"  # TODO: check unit
    colormap = ColorMapDef(
        # colormap="b_linear_wyor_100_45_c55",
        colormap="b_linear_kgy_5_95_c69",
    )
    legend = LegendDef(steps=7, decimals=0)
    related_carrier = CarrierEnum.ALL
    related_balance = BalanceEnum.SUPPLY

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
        per_region_fuel_supply = fuel_potential_and_production(var)
        per_region_heat_supply = residual_heat_potential(var)
        per_region_electricity_supply = (
            var.gqueries.total_electricity_produced.future / 1e9
        )  # MJ to PJ

        return (
            per_region_fuel_supply
            + per_region_heat_supply
            + per_region_electricity_supply
        )

    @staticmethod
    def map_aggregate(var: "Var"):
        per_region_fuel_supply = fuel_potential_and_production(var)
        per_region_heat_supply = residual_heat_potential(var)
        per_region_electricity_supply = (
            var.gqueries.total_electricity_produced.future / 1e9
        )  # MJ to PJ

        return (
            per_region_fuel_supply
            + per_region_heat_supply
            + per_region_electricity_supply
        )
