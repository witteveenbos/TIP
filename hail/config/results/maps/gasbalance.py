from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

from config.results.maps.gas_shared import fuel_demand, fuel_potential_and_production

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class GasBalanceNormalized(AbstractResultMap):

    key = "gas_balance_normalized"
    name = "Gasbalans (percentage)"
    unit = "%"
    colormap = ColorMapDef(
        colormap="b_diverging_gkr_60_10_c40",
        lower_limit=-100,
        upper_limit=100,
    )
    legend = LegendDef(steps=5, decimals=0)
    related_carrier = CarrierEnum.GAS
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
        fuel_potential = fuel_potential_and_production(var)
        per_region_fuel_demand = fuel_demand(var)
        balance = fuel_potential - per_region_fuel_demand
        balance_normalized = balance / per_region_fuel_demand * 100
        return balance_normalized

    @staticmethod
    def map_aggregate(var: "Var"):
        fuel_potential = fuel_potential_and_production(var)
        per_region_fuel_demand = fuel_demand(var)
        balance = fuel_potential - fuel_demand
        balance_normalized = balance / fuel_demand * 100
        total_fuel_demand = per_region_fuel_demand.sum_element_wise()

        return balance_normalized * per_region_fuel_demand / total_fuel_demand
