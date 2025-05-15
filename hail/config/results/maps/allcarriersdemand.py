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
)
from config.results.maps.gas_shared import fuel_demand


class AllCarriersBalanceNormalized(AbstractResultMap):

    key = "all_carriers_demand"
    name = "Totale energievraag"
    unit = "PJ"  # TODO: check unit
    colormap = ColorMapDef(
        colormap="b_linear_bmy_10_95_c78",
    )
    legend = LegendDef(steps=7, decimals=0)
    related_carrier = CarrierEnum.ALL
    related_balance = BalanceEnum.DEMAND

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
        per_region_fuel_demand = fuel_demand(var)
        per_region_heat_demand = heat_demand_from_sources(var)
        per_region_electricity_demand = (
            var.gqueries.total_electricity_consumed.future / 1e9
        )  # MJ to PJ

        return (
            per_region_fuel_demand
            + per_region_heat_demand
            + per_region_electricity_demand
        )

    @staticmethod
    def map_aggregate(var: "Var"):
        per_region_fuel_demand = fuel_demand(var)
        per_region_heat_demand = heat_demand_from_sources(var)
        per_region_electricity_demand = (
            var.gqueries.total_electricity_consumed.future / 1e9
        )  # MJ to PJ

        return (
            per_region_fuel_demand
            + per_region_heat_demand
            + per_region_electricity_demand
        )
