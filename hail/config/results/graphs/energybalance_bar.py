from typing import TYPE_CHECKING
from hail.models.calculate import GraphElement, GraphMeta
from hail.models.enums import plotTypes
from hail.result import AbstractResultGraph

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ElectricityBalanceBar(AbstractResultGraph):

    key = "energybalance_bar"
    name = "Energiebalans"
    unit = "GWh"  # TODO: make a unit Enum
    meta = GraphMeta(
        # if we don't supply a title, it will be the same as the name
        # if we don't supply a unit, it will be the same as the unit
        yLabelText="Energie",
        plotType=plotTypes.bar,
        xsectoring="demandSupply",
    )

    @staticmethod
    def graph(var: "Var"):
        graph_elements =  [
           
            # New graph based on the electricity Sankey: https://github.com/quintel/etmodel/blob/fa78a605b9722846337f604285311a5822733f7d/app/assets/javascripts/d3/sankey.coffee
            GraphElement(
                value=var.gqueries.import1_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import2_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import3_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import4_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import5_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import6_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import7_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import8_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import9_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import10_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import11_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.import12_to_network_in_sankey.future,
                color="#b71540",
                carrier="Import",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.other_renewables_to_network_in_sankey.future,
                color="#4465c6",
                carrier="Overige hernieuwbare bronnen",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.shortage_to_network_in_sankey.future,
                color="#DCDCDC",
                carrier="Elektriciteitstekort",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.solar_to_network_in_sankey.future,
                color="#ffcc00",
                carrier="Zon",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.hydrogen_to_network_in_sankey.future,
                color="#87cfeb",
                carrier="Waterstof",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.wind_to_network_in_sankey.future,
                color="#63A1C9",
                carrier="Wind",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.biomass_waste_greengas_to_network_in_sankey.future,
                color="#2ca02c",
                carrier="Biomassa, afval en groengas",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.fossil_to_network_in_sankey.future,
                color="#252525",
                carrier="Fossiel",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),
            GraphElement(
                value=var.gqueries.nuclear_to_network_in_sankey.future,
                color="#ff7f0e",
                carrier="Kernenergie",
                sector="Elektriciteitsbronnen",
                demandSupply="Aanbod",
            ),

            # Vraag, ook uit de Sankey
            GraphElement(
                value=var.gqueries.network_to_households_in_sankey.future,
                color="#FF6B6B",
                carrier="Huishoudens",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_buildings_in_sankey.future,
                color="#FFA07A",
                carrier="Gebouwen",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_transport_in_sankey.future,
                color="#45B7D1",
                carrier="Transport",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_industry_in_sankey.future,
                color="#4ECDC4",
                carrier="Industrie",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_agriculture_in_sankey.future,
                color="#98d8ad",
                carrier="Landbouw",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_p2g_in_sankey.future,
                color="#BB8FCE",
                carrier="Power-to-Gas",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_p2g_offshore_in_sankey.future,
                color="#855f96",
                carrier="Power-to-Gas offshore",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_curtailment_in_sankey.future,
                color="#F8B739",
                carrier="Curtailment",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_other_in_sankey.future,
                color="#95A5A6",
                carrier="Overig",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_bunkers_in_sankey.future,
                color="#8B4513",
                carrier="Bunkerbrandstoffen",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_loss_in_sankey.future,
                color="#DCDCDC",
                carrier="Verliezen",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export12_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export1_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export2_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export3_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export4_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export5_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export6_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export7_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export8_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export9_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export10_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),
            GraphElement(
                value=var.gqueries.network_to_export11_in_sankey.future,
                color="#B8B8D8",
                carrier="Export",
                sector="Elektriciteitsgebruik",
                demandSupply="Vraag",
            ),            
        ]
        # Conversion from PJ to GWh
        graph_elements = [graph_element.multiply_value(277.7778) for graph_element in graph_elements]
        return graph_elements

    @staticmethod
    def graph_aggregate(var: "Var"):

        raise NotImplementedError
