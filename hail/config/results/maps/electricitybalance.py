from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef, MapDataEntry, MapMetaData, MapResponse
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
        # Calculate domestic supply (excluding imports)
        total_supply = (
            # var.gqueries.import1_to_network_in_sankey.future + # this off course doens't count as supply, your importing it
            # var.gqueries.import2_to_network_in_sankey.future +
            # var.gqueries.import3_to_network_in_sankey.future +
            # var.gqueries.import4_to_network_in_sankey.future +
            # var.gqueries.import5_to_network_in_sankey.future +
            # var.gqueries.import6_to_network_in_sankey.future +
            # var.gqueries.import7_to_network_in_sankey.future +
            # var.gqueries.import8_to_network_in_sankey.future +
            # var.gqueries.import9_to_network_in_sankey.future +
            # var.gqueries.import10_to_network_in_sankey.future +
            # var.gqueries.import11_to_network_in_sankey.future +
            # var.gqueries.import12_to_network_in_sankey.future +
            var.gqueries.other_renewables_to_network_in_sankey.future +
            var.gqueries.shortage_to_network_in_sankey.future +
            var.gqueries.solar_to_network_in_sankey.future +
            var.gqueries.hydrogen_to_network_in_sankey.future +
            var.gqueries.wind_to_network_in_sankey.future +
            var.gqueries.biomass_waste_greengas_to_network_in_sankey.future +
            var.gqueries.fossil_to_network_in_sankey.future +
            var.gqueries.nuclear_to_network_in_sankey.future
        )
        
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
            # var.gqueries.network_to_export1_in_sankey.future + # This doesn't count as demand, your exporting it
            # var.gqueries.network_to_export2_in_sankey.future +
            # var.gqueries.network_to_export3_in_sankey.future +
            # var.gqueries.network_to_export4_in_sankey.future +
            # var.gqueries.network_to_export5_in_sankey.future +
            # var.gqueries.network_to_export6_in_sankey.future +
            # var.gqueries.network_to_export7_in_sankey.future +
            # var.gqueries.network_to_export8_in_sankey.future +
            # var.gqueries.network_to_export9_in_sankey.future +
            # var.gqueries.network_to_export10_in_sankey.future +
            # var.gqueries.network_to_export11_in_sankey.future +
            # var.gqueries.network_to_export12_in_sankey.future
        )
        
        # Return supply/demand ratio as percentage
        return (total_supply / total_demand) * 100

    @staticmethod
    def _get_supply(var: "Var"):
        """Helper method to calculate supply - used in make_map_aggregate"""
        total_supply = (
            var.gqueries.other_renewables_to_network_in_sankey.future +
            var.gqueries.shortage_to_network_in_sankey.future +
            var.gqueries.solar_to_network_in_sankey.future +
            var.gqueries.hydrogen_to_network_in_sankey.future +
            var.gqueries.wind_to_network_in_sankey.future +
            var.gqueries.biomass_waste_greengas_to_network_in_sankey.future +
            var.gqueries.fossil_to_network_in_sankey.future +
            var.gqueries.nuclear_to_network_in_sankey.future
        )
        return total_supply

    @staticmethod
    def _get_demand(var: "Var"):
        """Helper method to calculate demand - used in make_map_aggregate"""
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
        """
        Required by abstract base class but not used directly.
        We override make_map_aggregate instead to handle supply/demand aggregation separately.
        """
        raise NotImplementedError(
            "Use make_map_aggregate instead - balance requires separate supply/demand aggregation"
        )

    # Override the aggregation method to handle supply and demand separately for correct aggregation
    @classmethod
    def make_map_aggregate(cls, context: "ContextProvider") -> MapResponse:
        """Override to properly aggregate supply and demand separately before calculating ratio"""
        # Get supply and demand matrices at municipality level
        supply_matrix = cls._get_supply(context)
        demand_matrix = cls._get_demand(context)
        
        # Get the aggregator
        aggregator = context.aggregator
        
        # Aggregate both supply and demand to the target geographic level
        agg_supply = aggregator.aggregate(to_aggregate=supply_matrix, context=context)
        agg_demand = aggregator.aggregate(to_aggregate=demand_matrix, context=context)
        
        # Calculate the balance ratio at the aggregated level
        agg_balance = (agg_supply / agg_demand) * 100
        
        # Create colormap and metadata
        cm = cls.make_colormap(map_matrix=agg_balance)
        map_metadata = cls._make_metadata(colormap=cm)
        
        # Build the map response
        this_map = {
            region: MapDataEntry(
                gid=region,
                value=value,
                color=cm.get_color_for_value(value),
            )
            for region, value in zip(aggregator.region_ids, agg_balance)
        }
        
        return MapResponse(
            metadata=map_metadata,
            mapData=this_map,
        )
