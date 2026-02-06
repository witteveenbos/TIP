from typing import TYPE_CHECKING

from hail.models.matrix import Matrix

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

"""

Shared helper functions for electricity maps. Returns the total supply and demand based on the ETM Sankeys.
See also the sankey definition in hail/config/results/graphs/electricity_sankey_etm_spec.txt
This one is also used to create the relevant barcharts in hail/config/results/graphs/energybalance_bar.py


"""

def get_e_supply(var: "Var") -> Matrix:
    return (
        var.gqueries.other_renewables_to_network_in_sankey.future +
        var.gqueries.shortage_to_network_in_sankey.future +
        var.gqueries.solar_to_network_in_sankey.future +
        var.gqueries.hydrogen_to_network_in_sankey.future +
        var.gqueries.wind_to_network_in_sankey.future +
        var.gqueries.biomass_waste_greengas_to_network_in_sankey.future +
        var.gqueries.fossil_to_network_in_sankey.future +
        var.gqueries.nuclear_to_network_in_sankey.future
    ) * 277.7778  # conversion from PJ to GWh

def get_e_demand(var: "Var") -> Matrix:
    return (
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
    ) * 277.7778  # conversion from PJ to GWh