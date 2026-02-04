from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ElectricityBalanceNormalized(AbstractResultMap):

    key = "electricity_demand"
    name = "Elektriciteitsvraag"
    unit = "PJ"  # TODO: check unit
    colormap = ColorMapDef(
        colormap="b_linear_wyor_100_45_c55",
    )
    legend = LegendDef(steps=7, decimals=0)
    related_carrier = CarrierEnum.ELECTRICITY
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
        # Calculate local demand (excluding exports)
        total_demand = (
            var.gqueries.network_to_households_in_sankey.future +
            var.gqueries.network_to_buildings_in_sankey.future +
            var.gqueries.network_to_transport_in_sankey.future +
            var.gqueries.network_to_industry_in_sankey.future +
            var.gqueries.network_to_agriculture_in_sankey.future +
            var.gqueries.network_to_p2g_in_sankey.future +
            var.gqueries.network_to_p2g_offshore_in_sankey.future +
            var.gqueries.network_to_curtailment_in_sankey.future +
            var.gqueries.network_to_other_in_sankey.future +
            var.gqueries.network_to_bunkers_in_sankey.future +
            var.gqueries.network_to_loss_in_sankey.future
        )
        return total_demand

    @staticmethod
    def map_aggregate(var: "Var"):
        # Calculate local demand (excluding exports)
        total_demand = (
            var.gqueries.network_to_households_in_sankey.future +
            var.gqueries.network_to_buildings_in_sankey.future +
            var.gqueries.network_to_transport_in_sankey.future +
            var.gqueries.network_to_industry_in_sankey.future +
            var.gqueries.network_to_agriculture_in_sankey.future +
            var.gqueries.network_to_p2g_in_sankey.future +
            var.gqueries.network_to_p2g_offshore_in_sankey.future +
            var.gqueries.network_to_curtailment_in_sankey.future +
            var.gqueries.network_to_other_in_sankey.future +
            var.gqueries.network_to_bunkers_in_sankey.future +
            var.gqueries.network_to_loss_in_sankey.future
        )
        return total_demand
