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


class GridLoadSupply(AbstractResultMap):

    key = "grid_load_suppy"
    name = "Netbelasting door invoeding"
    unit = "%"  # TODO: make a unit Enum
    colormap = ColorMapDef(
        colormap="b_diverging_gkr_60_10_c40",
        lower_limit=0,
        upper_limit=250,
    )
    legend = LegendDef(steps=6, decimals=0)
    related_carrier = CarrierEnum.ELECTRICITY
    related_balance = BalanceEnum.SUPPLY
    related_area_div = AreaDivisionEnum.HSMS

    @staticmethod
    def map(var: "Var"):
        raise NotImplementedError("This map should never be called at GM-level")

    @staticmethod
    def map_aggregate(var: "Var"):

        residual_min = var.gqueries.residual_load_peak_min.future
        # Take the smaller than zero minimum because feedin is negative
        residual_netload_feedin = var.min(residual_min, var.Matrix(0))
        # Take the absolute value because we want to show this as relative load of station
        residual_netload_feedin = abs(residual_netload_feedin)

        return residual_netload_feedin

    # override the inherited method
    @classmethod
    def make_map_aggregate(cls, var: "Var") -> MapResponse:
        return make_grid_map(cls=cls, var=var, field_name="supply_capacity")
