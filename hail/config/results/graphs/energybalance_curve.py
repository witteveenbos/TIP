from typing import TYPE_CHECKING
from hail.models.calculate import GraphCurveElement, GraphMeta
from hail.models.enums import plotTypes
from hail.result import AbstractResultGraph

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class ElectricityBalanceCurve(AbstractResultGraph):

    key = "energybalance_curve"
    name = "Vermogensbalans elektriciteit"
    unit = "GW"  # TODO: make a unit Enum, check this unit
    meta = GraphMeta(
        # if we don't supply a title, it will be the same as the name
        # if we don't supply a unit, it will be the same as the unit
        yLabelText="Vermogen",
        plotType=plotTypes.line,
    )

    @staticmethod
    def graph(var: "Var"):
        return [
            # demand based on https://energytransitionmodel.com/output_elements/dynamic_demand_curve
            GraphCurveElement(
                value=var.gqueries.total_demand.future,
                color="#CC0000",
                name="Basislast elektriciteitsvraag",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_households_other_demand.future,
                color="#E84118",
                name="Huishoudens - Overig",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_households_space_heating_demand.future,
                color="#FF6B6B",
                name="Huishoudens - Ruimteverwarming",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_households_hot_water_demand.future,
                color="#FF0000",
                name="Huishoudens - Heet water",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_buildings_space_heating_demand.future,
                color="#F6E58D",
                name="Gebouwen - Ruimteverwarming",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_buildings_other_demand.future,
                color="#F9CA24",
                name="Gebouwen - Overig",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_ev_demand.future,
                color="#0984E3",
                name="Transport - Elektrische auto's",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_transport_other_demand.future,
                color="#74B9FF",
                name="Transport - Overig",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.mv_energy_heat_load_curve.future,
                color="#8B0000",
                name="Collectieve warmte",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_agriculture_demand.future,
                color="#6AB04C",
                name="Land- en Tuinbouw",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_other_demand.future,
                color="#FFA502",
                name="Overig",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_hv_network_loss.future,
                color="#D87093",
                name="Verliezen",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_industry_metals_demand.future,
                color="#666666",
                name="Industrie - Metaal",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_industry_chemical_demand.future,
                color="#2F3640",
                name="Industrie - Chemie",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_industry_other_demand.future,
                color="#353B48",
                name="Industrie - Overig",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_industry_transformation_demand.future,
                color="#9A9C9C",
                name="Industrie - Transformatie",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_other_flexibility_demand.future,
                color="#0AA1DD",
                name="Flexibiliteit - Conversie en opslag",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_energy_export_demand.future,
                color="#79DAE8",
                name="Flexibiliteit - Export",
                demandSupply="Vraag",
            ),
            GraphCurveElement(
                value=var.gqueries.merit_flexibility_curtailment_demand.future,
                color="#E8F9FD",
                name="Flexibiliteit - Productiebeperking",
                demandSupply="Vraag",
            ),
            # Supply side entries based on: https://energytransitionmodel.com/output_elements/merit_order_hourly_supply
            GraphCurveElement(
                value=var.gqueries.households_flexibility_p2p_electricity.future,
                color="#92896B",
                name="Thuisbatterijen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_supercritical_waste_mix.future,
                color="#006266",
                name="Afval-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_supercritical_ccs_waste_mix.future,
                color="#82002b",
                name="Afval-WKK + CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_supercritical_waste_mix.future,
                color="#CE7013",
                name="Afvalverbranding",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_supercritical_ccs_waste_mix.future,
                color="#CE7013",
                name="Afvalverbranding CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_combined_cycle_gas_power_fuelmix.future,
                color="#A4B0BE",
                name="Industriële gas STEG WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_engine_gas_power_fuelmix.future,
                color="#CED6E0",
                name="Industriële gasmotor-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_turbine_gas_power_fuelmix.future,
                color="#CED6E0",
                name="Industriële gasturbine-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_ultra_supercritical_coal.future,
                color="#485460",
                name="Industriële poederkolen-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.buildings_solar_pv_solar_radiation.future,
                color="#fed976",
                name="Zon op dak (gebouwen)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_geothermal.future,
                color="#94F95C",
                name="Geothermisch elektrisch",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_hydro_river.future,
                color="#0066ff",
                name="Waterkracht rivier",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_solar_csp_solar_radiation.future,
                color="#ced976",
                name="Geconcentreerde zonne-energie",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_solar_pv_solar_radiation.future,
                color="#ded976",
                name="Zon op land",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_solar_pv_offshore.future,
                color="#ffae00",
                name="Zon op zee",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_battery_solar_electricity.future,
                color="#FFF47D",
                name="Zon op land (batterij)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wind_turbine_coastal.future,
                color="#4292c6",
                name="Wind aan kust",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wind_turbine_inland.future,
                color="#9292c6",
                name="Wind op land",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wind_turbine_offshore.future,
                color="#7292c6",
                name="Wind op zee",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_hybrid_wind_turbine_offshore.future,
                color="#7487FF",
                name="Wind op zee (hybride)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_battery_wind_electricity.future,
                color="#63A1C9",
                name="Wind op land (batterij)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.households_solar_pv_solar_radiation.future,
                color="#eed976",
                name="Zon op dak (huishoudens)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_combined_cycle_network_gas.future,
                color="#0B7E6D",
                name="Gas STEG WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_ultra_supercritical_coal.future,
                color="#3BFAEB",
                name="Poederkolen-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_ultra_supercritical_cofiring_coal.future,
                color="#DFFBE5",
                name="Poederkolen-WKK met bijstook",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_ultra_supercritical_lignite.future,
                color="#131D1C",
                name="Bruinkolen-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_ccs_coal.future,
                color="#00A7B4",
                name="Kolenvergassing CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_ccs_network_gas.future,
                color="#407A8E",
                name="Gas STEG CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_coal.future,
                color="#C6E0E9",
                name="Kolenvergassing",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_network_gas.future,
                color="#9DD5FA",
                name="Gas STEG",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_engine_diesel.future,
                color="#295888",
                name="Dieselgenerator",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_engine_network_gas.future,
                color="#A3BFF6",
                name="Gasmotor",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_hydro_mountain.future,
                color="#629DF9",
                name="Waterkracht bergen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_nuclear_gen2_uranium_oxide.future,
                color="#4E60D1",
                name="Kern 2e Gen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_nuclear_gen3_uranium_oxide.future,
                color="#201A39",
                name="Kern 3e Gen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_nuclear_small_modular_reactor_uranium_oxide.future,
                color="#ca5ce0",
                name="Kern kleine modulaire reactor",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_supercritical_coal.future,
                color="#2F2661",
                name="Kolen conventioneel",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_turbine_network_gas.future,
                color="#B895F6",
                name="Gasturbine",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_ccs_coal.future,
                color="#9977EE",
                name="Poederkolen CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_coal.future,
                color="#AF63F1",
                name="Poederkolen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_cofiring_coal.future,
                color="#8643A9",
                name="Poederkolen met bijstook",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_crude_oil.future,
                color="#953ABC",
                name="Oliecentrale",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_lignite.future,
                color="#431B51",
                name="Bruinkolen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_network_gas.future,
                color="#D54CF7",
                name="Gas conventioneel",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_ultra_supercritical_oxyfuel_ccs_lignite.future,
                color="#F364F0",
                name="Bruinkolen 'oxyfuel' CCS",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.transport_car_using_electricity.future,
                color="#dd77bb",
                name="Batterijen in elektrische auto's",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.transport_bus_using_electricity.future,
                color="#f78fb4",
                name="Batterijen in elektrische bussen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.transport_van_using_electricity.future,
                color="#c91042",
                name="Batterijen in elektrische bestelbussen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.transport_truck_using_electricity.future,
                color="#db4270",
                name="Batterijen in elektrische vrachtwagens",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_interconnector_imported_electricity.future,
                color="#cccccc",
                name="Geïmporteerde elektriciteit",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_turbine_hydrogen.future,
                color="#09cff7",
                name="Waterstofturbine",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_flexibility_pumped_storage_electricity.future,
                color="#416B86",
                name="Opslag in stuwmeren",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_hydrogen.future,
                color="#00b2db",
                name="Waterstofcentrale STEG",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_flexibility_opac_electricity.future,
                color="#385ba6",
                name="Opslag in OPAC",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_flexibility_mv_batteries_electricity.future,
                color="#5a7bc4",
                name="Grootschalige batterijopslag",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_flexibility_flow_batteries_electricity.future,
                color="#162442",
                name="Opslag in flowbatterijen",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_engine_biogas.future,
                color="#FDE97B",
                name="Biogas-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_engine_network_gas.future,
                color="#F0904C",
                name="Gasmotor-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_wood_pellets_must_run.future,
                color="#AA2D02",
                name="Biomassa-WKK (must-run)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_wood_pellets_dispatchable.future,
                color="#FF612A",
                name="Biomassa-WKK (regelbaar)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_wood_pellets_ccs_must_run.future,
                color="#6F1D01",
                name="Biomassa-WKK + CCS (must-run)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_local_wood_pellets_ccs_dispatchable.future,
                color="#A24A2C",
                name="Biomassa-WKK + CCS (regelbaar)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wood_pellets_must_run.future,
                color="#5D7929",
                name="Biomassacentrale (must-run)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wood_pellets_dispatchable.future,
                color="#7EA437",
                name="Biomassacentrale (regelbaar)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wood_pellets_ccs_must_run.future,
                color="#304011",
                name="Biomassacentrale + CCS (must-run)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_wood_pellets_ccs_dispatchable.future,
                color="#8C947E",
                name="Biomassacentrale + CCS (regelbaar)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_wood_pellets.future,
                color="#771108",
                name="Industriële biomassa-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.industry_chp_turbine_hydrogen.future,
                color="#31a2c4",
                name="Industriële waterstofturbine-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_power_combined_cycle_coal_gas.future,
                color="#521b82",
                name="Kolengas STEG",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_chp_coal_gas.future,
                color="#7040c2",
                name="Kolengas-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.agriculture_chp_engine_dispatchable_network_gas.future,
                color="#783737",
                name="Landbouw gasmotor-WKK (regelbaar)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.agriculture_chp_engine_must_run_network_gas.future,
                color="#850404",
                name="Landbouw gasmotor-WKK (must-run)",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.agriculture_chp_engine_biogas.future,
                color="#cf5f5f",
                name="Landbouw biogas-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.agriculture_chp_wood_pellets.future,
                color="#fc0505",
                name="Landbouw biomassa-WKK",
                demandSupply="Aanbod",
            ),
            GraphCurveElement(
                value=var.gqueries.energy_load_shifting_industry.future,
                color="#F5B7B1",
                name="Verlaagde vraag in industrie",
                demandSupply="Aanbod",
            ),
        ]
            
    @staticmethod
    def graph_aggregate(var: "Var"):

        raise NotImplementedError    

