from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

from config.results.maps.heat_shared import (
    residual_heat_potential,
    heat_demand_from_sources,
)

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class HeatBalanceNormalized(AbstractResultMap):

    key = "heat_balance_normalized"
    name = "Warmtebalans (percentage)"
    unit = "%"
    colormap = ColorMapDef(
        colormap="b_diverging_gkr_60_10_c40",
        lower_limit=-100,
        upper_limit=100,
    )
    legend = LegendDef(steps=5, decimals=0)
    related_carrier = CarrierEnum.HEAT
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
        residual_heat = residual_heat_potential(var)
        heat_demand = heat_demand_from_sources(var)
        balance = residual_heat - heat_demand
        balance_normalized = balance / heat_demand * 100
        return balance_normalized

    @staticmethod
    def map_aggregate(var: "Var"):
        residual_heat = residual_heat_potential(var)
        per_region_heat_demand = heat_demand_from_sources(var)
        balance = residual_heat - per_region_heat_demand
        balance_normalized = balance / per_region_heat_demand * 100
        total_heat_demand = per_region_heat_demand.sum_element_wise()

        return balance_normalized * per_region_heat_demand / total_heat_demand
