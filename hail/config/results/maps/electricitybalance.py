from typing import TYPE_CHECKING

from hail.models.calculate import ColorMapDef, LegendDef, MapDataEntry, MapMetaData, MapResponse
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.result import AbstractResultMap

from config.results.maps.electricity_shared import get_e_supply, get_e_demand

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
  
    @classmethod
    def map(cls, var: "Var"):
        # Calculate domestic supply (excluding imports)
        total_supply = get_e_supply(var)
        total_demand = get_e_demand(var)
             
        # Return supply/demand ratio as percentage
        return (total_supply / total_demand) * 100


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
        supply_matrix = get_e_supply(context)
        demand_matrix = get_e_demand(context)
        
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
