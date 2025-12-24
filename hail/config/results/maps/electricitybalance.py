from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ElectricityBalanceNormalized(AbstractResultMap):

    key = "electricity_balance_normalized"
    name = "Elektriciteitsbalans, aanbod-vraag ratio (%)"
    unit = "%"  # TODO: make a unit Enum
    colormap = ColorMapDef(
        colormap="b_diverging_bwr_55_98_c37",
        lower_limit=0,
        upper_limit=200,
        reverse=True
    )
    legend = LegendDef(steps=9, decimals=0)
    related_carrier = CarrierEnum.ELECTRICITY
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

        return var.gqueries.share_of_electricity_generated_domestically.future * 100

    @staticmethod
    def map_aggregate(var: "Var"):

        per_region_balance = (
            var.gqueries.share_of_electricity_generated_domestically.future * 100
        )
        per_region_generation = var.gqueries.total_electricity_produced.future
        total_generation = (
            var.gqueries.total_electricity_produced.future
        ).sum_element_wise()

        return per_region_balance * per_region_generation / total_generation
