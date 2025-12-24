import logging
from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef, MapResponse
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

from config.results.maps._shared import make_grid_map

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class GridLoadDemand(AbstractResultMap):

    key = "grid_load_demand"
    name = "Netbelasting door afname"
    unit = "%"  # TODO: make a unit Enum
    colormap = ColorMapDef(
        colormap="b_linear_wyor_100_45_c55",
        lower_limit=0,
        upper_limit=250,
    )
    legend = LegendDef(steps=6, decimals=0)
    related_carrier = CarrierEnum.ELECTRICITY
    related_balance = BalanceEnum.DEMAND
    related_area_div = AreaDivisionEnum.HSMS

    @staticmethod
    def map(var: "Var"):
        raise NotImplementedError("This map should never be called at GM-level")

    @staticmethod
    def map_aggregate(var: "Var"):

        residual_max = var.gqueries.residual_load_peak_max.future
        # Take the larger than zero maximum because demand is positive
        residual_netload_demand = var.max(residual_max, var.Matrix(0))
        # Take the absolute value because we want to show this as relative load of station
        residual_netload_demand = abs(residual_netload_demand)
        logging.info(f"residual_netload_demand: {residual_netload_demand}")
        return residual_netload_demand

    # override the inherited method
    @classmethod
    def make_map_aggregate(cls, var: "Var") -> MapResponse:
        return make_grid_map(cls=cls, var=var, field_name="demand_capacity")
