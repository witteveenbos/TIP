from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import besparing_in_utiliteiten

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider

import logging


class BesparingWarmtevraagUtiliteiten(AbstractDevelopment):

    name = "Besparing warmtevraag"
    key = "utiliteiten_besparing_warmtevraag"
    unit = "%"
    dev_type = DevelomentType.CONTINUOUS
    group = besparing_in_utiliteiten

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # De maximale reductie in warmtevraag is gecapt op 70% van het heden,
        # in navolging van de implementatie bij huishoudens
        return var.Matrix(70)

    @staticmethod
    def default(var: "Var"):
        # Berekent de procentuele afname tussen de toekomstige en huidige waarde van de finale energievraag voor ruimteverwarming in utiliteiten
        # De minimale waarde van de besparing is 0 (bij gelijkblijvende of stijgende ruimteverwarmingsvraag)
        # NB: hier wordt de FINALE warmtevraag gebruikt, omdat er (vooralsnog) geen queries bestaan in het ETM
        # voor de nuttige warmtevraag van utiliteiten
        space_heating_demand_present = (
            var.gqueries.heat_demand_buildings_in_use_of_final_demand_in_buildings.present
        )
        space_heating_demand_future = (
            var.gqueries.heat_demand_buildings_in_use_of_final_demand_in_buildings.future
        )

        default_from_etm = (
            100.0
            * (space_heating_demand_present - space_heating_demand_future)
            / space_heating_demand_present
        )
        demand_reduction = var.max(
            default_from_etm,
            var.Matrix(0),
        )

        # logging.error(f"default_from_etm: {default_from_etm}")
        # logging.error(f"demand_reduction: {demand_reduction}")

        return demand_reduction

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Deze method vermindert de typische warmtevraag van alle utiliteiten met het ingestelde percentage uit de tool
        # Zo wordt de totale nuttige warmtevraag met het ingestelde percentage verminderd.

        # raise NotImplementedError
        slider = var.ui.utiliteiten_besparing_warmtevraag

        reduction_factor = (100.0 - slider) / 100.0

        # Haal de typische warmtevraagsliders als object op
        insulation_level_existing_buildings = (
            var.inputs.buildings_insulation_level_buildings_present
        )
        insulation_level_new_buildings = (
            var.inputs.buildings_insulation_level_buildings_future
        )

        ## Haal huidige waarden van de typische warmtevraagsliders op
        insulation_level_existing_buildings_value_etm = (
            insulation_level_existing_buildings.user
        )
        insulation_level_new_buildings_value_etm = insulation_level_new_buildings.user

        ## Haal de minimale waarde van de typische warmtevraagsliders op
        insulation_level_existing_buildings_min_value = (
            insulation_level_existing_buildings.min
        )
        insulation_level_new_buildings_min_value = insulation_level_new_buildings.min

        ## Stel nieuwe waarde van de typische warmtevraagslider in op 100 - reductiepercentage
        ## tenzij hiermee de ondergrens van bijv 25 kWh/m2 van slider bereikt wordt.
        ## Houd in dat geval de ondergrens aan.
        insulation_level_existing_buildings_target = var.max(
            insulation_level_existing_buildings_value_etm * reduction_factor,
            insulation_level_existing_buildings_min_value,
        )

        insulation_level_new_buildings_target = var.max(
            insulation_level_new_buildings_value_etm * reduction_factor,
            insulation_level_new_buildings_min_value,
        )

        ## Geef nieuwe waarde alleen door aan als de gebruiker daadwerkelijk een nieuwe waarde heeft ingesteld
        ## Anders: None
        insulation_level_existing_buildings_target = (
            insulation_level_existing_buildings_target
            * var.ui.utiliteiten_besparing_warmtevraag.mask
        )
        insulation_level_new_buildings_target = (
            insulation_level_new_buildings_target
            * var.ui.utiliteiten_besparing_warmtevraag.mask
        )

        return {
            insulation_level_existing_buildings: insulation_level_existing_buildings_target,
            insulation_level_new_buildings: insulation_level_new_buildings_target,
        }

    @staticmethod
    def aggregate(var: "Var"):
        # Berekent een gewogen gemiddelde van de bespaarde energievraag voor ruimteverwarming in utiliteiten
        # Hierbij wordt de finale warmtevraag voor ruimteverwarming in de huidige situatie als gewicht genomen

        # Bereken de procentuele afname tussen de toekomstige en huidige waarde van de finale energievraag voor ruimteverwarming in utiliteiten
        space_heating_demand_present = (
            var.gqueries.heat_demand_buildings_in_use_of_final_demand_in_buildings.present
        )
        space_heating_demand_future = (
            var.gqueries.heat_demand_buildings_in_use_of_final_demand_in_buildings.future
        )

        demand_reduction = var.max(
            -1.0
            * (space_heating_demand_future - space_heating_demand_present)
            / space_heating_demand_present,
            var.Matrix(0),
        )

        # override the calculated value with the value from the UI, if it exists
        demand_reduction = var.ui.utiliteiten_besparing_warmtevraag | demand_reduction

        # Bereken de gewichten
        space_heating_demand_weights = space_heating_demand_present / sum(
            space_heating_demand_present
        )

        # Bereken gewogen gemiddelden
        weighted_demand_reduction = space_heating_demand_weights * demand_reduction

        return weighted_demand_reduction
