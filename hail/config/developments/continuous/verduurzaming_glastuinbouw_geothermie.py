from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import verduurzaming_bestaande_glastuinbouw

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class Geothermie(AbstractDevelopment):

    name = "Geothermie"
    key = "geothermie"
    unit = "%"
    dev_type = DevelomentType.CONTINUOUS
    group = verduurzaming_bestaande_glastuinbouw

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):

        geothermal = var.inputs.agriculture_geothermal_share.max

        return geothermal

    @staticmethod
    def default(var: "Var"):
        # Toon het aandeel duurzame warmtetechnologieën in de landbouw.
        # Deze zijn gedefinieerd als 100 - niet-duurzame technologieën, te weten:
        # olieketel, gasketel en lokale warmte (WKK)

        # Haal de aandelen niet-duurzame technologieën op
        gas_share = var.inputs.agriculture_burner_network_gas_share.user_original
        olie_share = var.inputs.agriculture_burner_crude_oil_share.user_original
        lokale_warmte_share = (
            var.inputs.agriculture_final_demand_local_steam_hot_water_share.user_original
        )

        niet_duurzaam_share = gas_share + olie_share + lokale_warmte_share

        # Stel het aandeel duurzame warmtetechnologieën in
        duurzaam_share = 100.0 - niet_duurzaam_share

        return duurzaam_share

    @staticmethod
    def sets_ETM_value(var: "Var"):
        # Pas het aandeel geothermie aan op basis van de ingevoerde waarde uit de tool.
        # Het restant wordt op gasketels gezet (niet-duurzaam)

        # 1. Haal de ETM-sliders op als objecten
        ## Haal de ETM-sliders van de ruimtetechnologiemix op als object
        gas_share = var.inputs.agriculture_burner_network_gas_share
        olie_share = var.inputs.agriculture_burner_crude_oil_share
        biomassa_share = var.inputs.agriculture_burner_wood_pellets_share
        waterstof_share = var.inputs.agriculture_burner_hydrogen_share
        wp_wko_share = var.inputs.agriculture_heatpump_water_water_ts_electricity_share
        geothermie_share = var.inputs.agriculture_geothermal_share
        warmtenet_ht_share = (
            var.inputs.agriculture_final_demand_ht_central_steam_hot_water_share
        )
        warmtenet_mt_share = (
            var.inputs.agriculture_final_demand_mt_central_steam_hot_water_share
        )
        lokale_warmte_share = (
            var.inputs.agriculture_final_demand_local_steam_hot_water_share
        )
        wp_water_water_share = (
            var.inputs.agriculture_heatpump_water_water_electricity_share
        )

        # 2. Haal de sliderwaarde uit de tool op
        slider = var.ui.geothermie

        # 3. Vertaal de sliderwaarde naar het aandeel geothermie en gasketels
        geothermie_share_target = slider
        gas_share_target = 100.0 - geothermie_share_target

        # 4. Stel alle andere technologieën in op 0
        olie_share_target = var.Matrix(0)
        biomassa_share_target = var.Matrix(0)
        waterstof_share_target = var.Matrix(0)
        wp_wko_share_target = var.Matrix(0)
        warmtenet_ht_share_target = var.Matrix(0)
        warmtenet_mt_share_target = var.Matrix(0)
        lokale_warmte_share_target = var.Matrix(0)
        wp_water_water_share_target = var.Matrix(0)

        is_changed = slider.mask

        return {
            gas_share: gas_share_target * is_changed,
            olie_share: olie_share_target * is_changed,
            biomassa_share: biomassa_share_target * is_changed,
            waterstof_share: waterstof_share_target * is_changed,
            wp_wko_share: wp_wko_share_target * is_changed,
            geothermie_share: geothermie_share_target * is_changed,
            warmtenet_ht_share: warmtenet_ht_share_target * is_changed,
            warmtenet_mt_share: warmtenet_mt_share_target * is_changed,
            lokale_warmte_share: lokale_warmte_share_target * is_changed,
            wp_water_water_share: wp_water_water_share_target * is_changed,
        }

    @staticmethod
    def aggregate(var: "Var"):
        # Berekent een gewogen gemiddelde van het aandeel geothermie in de landbouw
        # Hierbij wordt de finale energievraag van de landbouw in de huidige situatie als gewicht genomen

        geothermal_shares = (
            var.ui.geothermie | var.inputs.agriculture_geothermal_share.user
        )

        # Bereken de gewichten
        final_demand_agriculture = var.gqueries.final_demand_from_agriculture.present
        final_demand_agriculture_weights = (
            final_demand_agriculture * geothermal_shares / sum(final_demand_agriculture)
        )

        # Bereken gewogen gemiddelde
        geothermal_shares_weighted = (
            final_demand_agriculture_weights * final_demand_agriculture
        )

        return geothermal_shares_weighted
