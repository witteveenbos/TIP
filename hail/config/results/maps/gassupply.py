from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

from config.results.maps.gas_shared import fuel_potential_and_production


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class GasSupplyAbsolute(AbstractResultMap):

    key = "gas_supply"
    name = "Gasproductie"
    unit = "PJ"  # TODO: check unit
    colormap = ColorMapDef(
        colormap="b_linear_blue_95_50_c20",
    )
    legend = LegendDef(steps=7, decimals=0)
    related_carrier = CarrierEnum.GAS
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
        return fuel_potential_and_production(var)

    @staticmethod
    def map_aggregate(var: "Var"):
        return fuel_potential_and_production(var)
