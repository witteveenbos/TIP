from typing import TYPE_CHECKING
from math import floor
from config.developments.continuous._groups import verduurzaming_bestaande_bouw
from config.developments.sectoral._groups import nieuwbouwprojecten
from hail.models.matrix import Matrix


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider | Matrix

import logging


def bestaand_allelectric_default(var: "Var"):
    # All-electric includes: air heat pumps, ground heat pumps, pvt heat pumps, aquathermal heat pumps and e-boilers
    number_homes_lwp = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_heatpump_air_water_electricity.future
    )

    number_homes_bwp = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_heatpump_ground_water_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_heatpump_ground_water_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_heatpump_ground_water_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_heatpump_ground_water_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_heatpump_ground_water_electricity.future
    )

    number_homes_pvt = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_heatpump_pvt_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_heatpump_pvt_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_heatpump_pvt_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_heatpump_pvt_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_heatpump_pvt_electricity.future
    )

    number_homes_aquathermie = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_heatpump_surface_water_water_ts_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_heatpump_surface_water_water_ts_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_heatpump_surface_water_water_ts_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_heatpump_surface_water_water_ts_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_heatpump_surface_water_water_ts_electricity.future
    )

    number_homes_e_boiler = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_electricity.future
    )

    return (
        number_homes_lwp
        + number_homes_bwp
        + number_homes_pvt
        + number_homes_aquathermie
        + number_homes_e_boiler
    )


def bestaand_hybride_default(var: "Var"):
    # Hybrid includes hybrid heat pumps on gas and hybrid heat pumps on hydrogen
    number_of_homes_hybrid_network_gas = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_hybrid_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_hybrid_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_hybrid_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_hybrid_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_hybrid_heatpump_air_water_electricity.future
    )

    number_of_homes_hybrid_hydrogen = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
    )

    return number_of_homes_hybrid_network_gas + number_of_homes_hybrid_hydrogen


def bestaand_warmtenet_default(var: "Var"):
    # District heating includes HT, MT and LT district heating networks
    number_of_homes_heat_network_ht = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_district_heating_ht_steam_hot_water.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_district_heating_ht_steam_hot_water.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_district_heating_ht_steam_hot_water.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_district_heating_ht_steam_hot_water.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_district_heating_ht_steam_hot_water.future
    )

    number_of_homes_heat_network_mt = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_district_heating_mt_steam_hot_water.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_district_heating_mt_steam_hot_water.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_district_heating_mt_steam_hot_water.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_district_heating_mt_steam_hot_water.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_district_heating_mt_steam_hot_water.future
    )

    number_of_homes_heat_network_lt = (
        var.gqueries.number_of_houses_before_1945_with_space_heater_district_heating_lt_steam_hot_water.future
        + var.gqueries.number_of_houses_1945_1964_with_space_heater_district_heating_lt_steam_hot_water.future
        + var.gqueries.number_of_houses_1965_1984_with_space_heater_district_heating_lt_steam_hot_water.future
        + var.gqueries.number_of_houses_1985_2004_with_space_heater_district_heating_lt_steam_hot_water.future
        + var.gqueries.number_of_houses_2005_present_with_space_heater_district_heating_lt_steam_hot_water.future
    )

    return (
        number_of_homes_heat_network_ht
        + number_of_homes_heat_network_mt
        + number_of_homes_heat_network_lt
    )


def nieuwbouw_warmtenet_default(var: "Var"):

    total = (
        var.gqueries.number_of_houses_future_with_space_heater_district_heating_ht_steam_hot_water.future
        + var.gqueries.number_of_houses_future_with_space_heater_district_heating_mt_steam_hot_water.future
        + var.gqueries.number_of_houses_future_with_space_heater_district_heating_lt_steam_hot_water.future
    )

    return total


def nieuwbouw_hybride_default(var: "Var"):

    number_homes_hybride_gas = (
        var.gqueries.number_of_houses_future_with_space_heater_hybrid_heatpump_air_water_electricity.future
    )

    number_homes_hybride_waterstof = (
        var.gqueries.number_of_houses_future_with_space_heater_hybrid_hydrogen_heatpump_air_water_electricity.future
    )

    total = number_homes_hybride_gas + number_homes_hybride_waterstof

    return total


def nieuwbouw_allelectric_default(var: "Var"):
    # All-electric omvat: luchtwarmtepompen, bodemwarmtepompen, pvt-warmtepompen, aquathermie-warmtepompen en e-boilers

    number_homes_lwp = (
        var.gqueries.number_of_houses_future_with_space_heater_heatpump_air_water_electricity.future
    )

    number_homes_bwp = (
        var.gqueries.number_of_houses_future_with_space_heater_heatpump_ground_water_electricity.future
    )

    number_homes_pvt = (
        var.gqueries.number_of_houses_future_with_space_heater_heatpump_pvt_electricity.future
    )

    number_homes_aquathermie = (
        var.gqueries.number_of_houses_future_with_space_heater_heatpump_surface_water_water_ts_electricity.future
    )

    number_homes_e_boiler = (
        var.gqueries.number_of_houses_future_with_space_heater_electricity.future
    )

    total = (
        number_homes_lwp
        + number_homes_bwp
        + number_homes_pvt
        + number_homes_aquathermie
        + number_homes_e_boiler
    )

    return total


def set_heat_sliders_households(var: "Var"):
    # Deze method stelt twee soorten ETM-sliders in:
    # a) de ruimtetechnologiemix in huishoudens;
    # b) het aantal nieuwbouwwoningen per woningtype

    # 1. Haal de ETM-sliders op als objecten
    ## Haal de ETM-sliders van de ruimtetechnologiemix op als object
    cv_share = var.inputs.households_heater_combined_network_gas_share
    cv_waterstof_share = var.inputs.households_heater_combined_hydrogen_share
    warmtenet_ht_share = (
        var.inputs.households_heater_district_heating_ht_steam_hot_water_share
    )
    warmtenet_mt_share = (
        var.inputs.households_heater_district_heating_mt_steam_hot_water_share
    )
    warmtenet_lt_share = (
        var.inputs.households_heater_district_heating_lt_steam_hot_water_share
    )
    lwp_share = var.inputs.households_heater_heatpump_air_water_electricity_share
    bwp_share = var.inputs.households_heater_heatpump_ground_water_electricity_share
    aquathermie_share = (
        var.inputs.households_heater_heatpump_surface_water_water_ts_electricity_share
    )
    hybride_gas_share = (
        var.inputs.households_heater_hybrid_heatpump_air_water_electricity_share
    )
    hybride_waterstof_share = (
        var.inputs.households_heater_hybrid_hydrogen_heatpump_air_water_electricity_share
    )
    pvt_share = var.inputs.households_heater_heatpump_pvt_electricity_share
    houtpellet_share = var.inputs.households_heater_wood_pellets_share
    e_boiler_share = var.inputs.households_heater_electricity_share
    gasketel_share = var.inputs.households_heater_network_gas_share

    ## Haal de ETM-sliders van de aantallen nieuwe woningen per woningtype op als object
    number_new_apartments = var.inputs.households_number_of_apartments_future
    number_new_detached_houses = var.inputs.households_number_of_detached_houses_future
    number_new_semi_detached_houses = (
        var.inputs.households_number_of_semi_detached_houses_future
    )
    number_new_terraced_houses = var.inputs.households_number_of_terraced_houses_future

    ## Haal de totale bestaande woningvoorraad op zoals oorspronkelijk ingesteld in het ETM
    ## Dit kan niet uit de tool zelf gehaald worden, omdat bestaande bouw met CV-ketels ontbreekt
    ## in de groep verduurzaming_bestaande_bouw
    number_existing_residences = (
        var.gqueries.number_of_residences_before_1945.future
        + var.gqueries.number_of_residences_1945_1964.future
        + var.gqueries.number_of_residences_1965_1984.future
        + var.gqueries.number_of_residences_1985_2004.future
        + var.gqueries.number_of_residences_2005_present.future
    )

    # 2. Bereken de verdeling van woningtypen in de bestaande bouw uit het ETM
    # op basis van de huidige situatie
    number_existing_residences_etm = var.gqueries.number_of_residences.present
    apartments_share = (
        var.gqueries.number_of_apartments.present / number_existing_residences_etm
    )
    detached_houses_share = (
        var.gqueries.number_of_detached_houses.present / number_existing_residences_etm
    )
    semi_detached_houses_share = (
        var.gqueries.number_of_semi_detached_houses.present
        / number_existing_residences_etm
    )
    terraced_houses_share = (
        var.gqueries.number_of_terraced_houses.present / number_existing_residences_etm
    )

    # 3. Haal relevante instellingen op uit de tool
    ## Haal het totaal aantal woningen op zoals ingesteld in de tool
    ## Dit betreft het totaal aantal nieuwbouwwoningenl
    number_new_residences = var.groups.nieuwbouwprojecten.TOTAL
    number_of_homes_unchanged = var.gqueries.number_of_residences.future

    ## Als er wijzigingen zijn in het aantal nieuwbouwwoningen, pas dit dan toe om tot het nieuwe aantal woningen te komen
    # als dat niet zo is; ga verder met het aantal woningen zoals ingesteld in het ETM (toekomstig)
    number_of_homes_total = (
        number_existing_residences + number_new_residences
    ) * number_new_residences.mask | number_of_homes_unchanged

    ## Haal de toolinstellingen van het aantal huizen voor alle oplossingen behalve cv-ketels op
    ## voor zowel bestaande bouw als nieuwbouw
    either_slider_all_electric = (
        var.ui.verduurzaming_bestaand_all_electric + var.ui.all_electric
    )
    either_slider_hybride = var.ui.verduurzaming_bestaand_hybride + var.ui.hybride
    either_slider_warmtenet = var.ui.verduurzaming_bestaand_warmtenet + var.ui.warmtenet

    # Logical flow: take the slider value if it is set, otherwise take the default value
    # but only let this propogate if either of the sliders is set
    slider_all_e = (
        # bestaand
        (var.ui.verduurzaming_bestaand_all_electric | bestaand_allelectric_default(var))
        # nieuwbouw
        + (var.ui.all_electric | nieuwbouw_allelectric_default(var))
    ) * either_slider_all_electric.mask
    slider_hybride = (
        # bestaand
        (var.ui.verduurzaming_bestaand_hybride | bestaand_hybride_default(var))
        # nieuwbouw
        + (var.ui.hybride | nieuwbouw_hybride_default(var))
    ) * either_slider_hybride.mask
    slider_warmtenet = (
        # bestaand
        (var.ui.verduurzaming_bestaand_warmtenet | bestaand_warmtenet_default(var))
        # nieuwbouw
        + (var.ui.warmtenet | nieuwbouw_warmtenet_default(var))
    ) * either_slider_warmtenet.mask
    # 4. Stel het aantal nieuwbouwwoningen per woningtype voor het ETM in
    # Effectief is dit alleen relevant als in de tool het aantal nieuwbouwwoningen wijzigt
    number_new_apartments_target = number_new_residences * apartments_share
    number_new_detached_houses_target = number_new_residences * detached_houses_share
    number_new_semi_detached_houses_target = (
        number_new_residences * semi_detached_houses_share
    )
    number_new_terraced_houses_target = number_new_residences * terraced_houses_share

    # 5. Stel de nieuwe ETM-waarden voor de ruimtetechnologiemix in

    ## Stel aandelen van afzonderlijke all-electric oplossingen voor ETM in
    ## All-e wordt in vaste verhouding toegewezen aan luchtwarmtepomp en bodemwarmtepomp
    ## De overige oplossingen worden op 0 gezet
    lwp_share_in_all_e = 0.7
    bwp_share_in_all_e = 1.0 - lwp_share_in_all_e

    all_e_share = slider_all_e / number_of_homes_total
    lwp_share_target = all_e_share * lwp_share_in_all_e * 100.0
    bwp_share_target = all_e_share * bwp_share_in_all_e * 100.0

    pvt_share_target = var.Matrix(0)
    aquathermie_share_target = var.Matrix(0)
    e_boiler_share_target = var.Matrix(0)

    ## Stel aandelen van de overige technologieën in de mix in
    ## Hybride: alleen de gasvariant, waterstof op 0
    hybride_gas_share_target = slider_hybride / number_of_homes_total * 100.0
    hybride_waterstof_share_target = var.Matrix(0)

    ## Warmtenet: alleen MT-warmtenet instellen, de overige temperatuurniveaus op 0
    warmtenet_mt_share_target = slider_warmtenet / number_of_homes_total * 100.0
    warmtenet_ht_share_target = var.Matrix(0)
    warmtenet_lt_share_target = var.Matrix(0)

    ## Overige oplossingen: stel in op 0
    cv_waterstof_share_target = var.Matrix(0)
    houtpellet_share_target = var.Matrix(0)

    ## CV-ketels: alleen daadwerkelijke CV-ketels, gasketels op 0

    ### De share groups in het ETM moeten altijd op precies 100% uitkomen
    ### Pas daarom een correctiefactor toe als (door afronding) de overige drie categorieën op >100% uitkomen
    total_share_target_excluding_cv = (
        lwp_share_target
        + bwp_share_target
        + hybride_gas_share_target
        + warmtenet_mt_share_target
    )

    if any(total_share_target_excluding_cv > 100):
        # Definieer eerst de terugvaloptie voor cv_share_target
        cv_share_target = 100.0 - total_share_target_excluding_cv
        gasketel_share_target = var.Matrix(0)

        correction_required = True
        correction_factor = total_share_target_excluding_cv / 100.0

        ### Rond de nieuwe target shares naar beneden af op 1 decimaal
        lwp_share_target_corrected = (
            floor(lwp_share_target / correction_factor * 10.0) / 10.0
        )
        bwp_share_target_corrected = (
            floor(bwp_share_target / correction_factor * 10.0) / 10.0
        )
        hybride_gas_share_target_corrected = (
            floor(hybride_gas_share_target / correction_factor * 10.0) / 10.0
        )
        warmtenet_mt_share_target_corrected = (
            floor(warmtenet_mt_share_target / correction_factor * 10.0) / 10.0
        )

        ### Door floor kan er alsnog een verschil met 100% ontstaan zijn.
        ### Bereken daarom het verschil dat aan CV-ketels toegewezen moet worden
        remnant = 100.0 - (
            lwp_share_target_corrected
            + bwp_share_target_corrected
            + hybride_gas_share_target_corrected
            + warmtenet_mt_share_target_corrected
        )
    else:
        correction_required = False

    if correction_required:
        # Voer bovenstaande normalisatie alleen uit in gemeenten waar dit daadwerkelijk moet
        correction_mask = (total_share_target_excluding_cv > 100).mask
        lwp_share_target = (
            lwp_share_target_corrected * correction_mask
        ) | lwp_share_target
        bwp_share_target = (
            bwp_share_target_corrected * correction_mask
        ) | bwp_share_target
        hybride_gas_share_target = (
            hybride_gas_share_target_corrected * correction_mask
        ) | hybride_gas_share_target
        warmtenet_mt_share_target = (
            warmtenet_mt_share_target_corrected * correction_mask
        ) | warmtenet_mt_share_target
        cv_share_target = (remnant * correction_mask) | cv_share_target
    else:
        cv_share_target = 100.0 - total_share_target_excluding_cv
        gasketel_share_target = var.Matrix(0)

    # 6. Maskeer de naar alleen de gemeentes met aanpassingen
    is_changed = (slider_all_e | slider_hybride | slider_warmtenet).mask

    # 7. Geef alle berekende outputs terug
    return {
        number_new_apartments: number_new_apartments_target,
        number_new_detached_houses: number_new_detached_houses_target,
        number_new_semi_detached_houses: number_new_semi_detached_houses_target,
        number_new_terraced_houses: number_new_terraced_houses_target,
        cv_share: cv_share_target * is_changed,
        cv_waterstof_share: cv_waterstof_share_target * is_changed,
        warmtenet_ht_share: warmtenet_ht_share_target * is_changed,
        warmtenet_mt_share: warmtenet_mt_share_target * is_changed,
        warmtenet_lt_share: warmtenet_lt_share_target * is_changed,
        lwp_share: lwp_share_target * is_changed,
        bwp_share: bwp_share_target * is_changed,
        aquathermie_share: aquathermie_share_target * is_changed,
        hybride_gas_share: hybride_gas_share_target * is_changed,
        hybride_waterstof_share: hybride_waterstof_share_target * is_changed,
        pvt_share: pvt_share_target * is_changed,
        houtpellet_share: houtpellet_share_target * is_changed,
        e_boiler_share: e_boiler_share_target * is_changed,
        gasketel_share: gasketel_share_target * is_changed,
    }


def set_heat_sliders_buildings(var: "Var"):
    # Deze method stelt de ruimtetechnologiemix voor bestaande utiliteiten in

    # 1. Haal de ETM-sliders op als objecten
    ## Haal de ETM-sliders van de ruimtetechnologiemix op als object
    cv_share = var.inputs.buildings_space_heater_network_gas_share
    cv_waterstof_share = var.inputs.buildings_space_heater_combined_hydrogen_share
    warmtenet_ht_share = (
        var.inputs.buildings_space_heater_district_heating_ht_steam_hot_water_share
    )
    warmtenet_mt_share = (
        var.inputs.buildings_space_heater_district_heating_mt_steam_hot_water_share
    )
    warmtenet_lt_share = (
        var.inputs.buildings_space_heater_district_heating_lt_steam_hot_water_share
    )
    lwp_gas_share = (
        var.inputs.buildings_space_heater_heatpump_air_water_network_gas_share
    )
    lwp_share = var.inputs.buildings_space_heater_heatpump_air_water_electricity_share
    hybride_gas_share = (
        var.inputs.buildings_space_heater_hybrid_heatpump_air_water_electricity_share
    )
    hybride_waterstof_share = (
        var.inputs.buildings_space_heater_hybrid_hydrogen_heatpump_air_water_electricity_share
    )
    bwp_share = (
        var.inputs.buildings_space_heater_collective_heatpump_water_water_ts_electricity_share
    )
    aquathermie_share = (
        var.inputs.buildings_space_heater_heatpump_surface_water_water_ts_electricity_share
    )
    e_boiler_share = var.inputs.buildings_space_heater_electricity_share
    houtpellet_share = var.inputs.buildings_space_heater_wood_pellets_share

    ## Haal aantal gebouwen uit de tool op
    number_of_buildings_present = var.inputs.buildings_number_of_buildings_present.max

    # 2. Haal relevante instellingen op uit de tool
    ## Aantal ingestelde utiliteiten per warmteoplossing op
    slider_all_e = var.ui.utiliteiten_all_electric
    slider_hybride = var.ui.utiliteiten_hybride
    slider_warmtenet = var.ui.utiliteiten_warmtenet

    # 3. Stel de nieuwe ETM-waarden voor de ruimtetechnologiemix in
    ## Stel aandelen van afzonderlijke all-electric oplossingen voor ETM in
    ## All-e wordt in vaste verhouding toegewezen aan luchtwarmtepomp en bodemwarmtepomp
    ## De overige oplossingen worden op 0 gezet
    lwp_share_in_all_e = 0.7
    bwp_share_in_all_e = 1.0 - lwp_share_in_all_e

    all_e_share = slider_all_e / number_of_buildings_present
    lwp_share_target = all_e_share * lwp_share_in_all_e * 100.0
    bwp_share_target = all_e_share * bwp_share_in_all_e * 100.0

    aquathermie_share_target = var.Matrix(0)
    e_boiler_share_target = var.Matrix(0)

    ## Stel aandelen van de overige technologieën in de mix in
    ## Hybride: alleen de gasvariant, waterstof op 0
    hybride_gas_share_target = slider_hybride / number_of_buildings_present * 100.0
    hybride_waterstof_share_target = var.Matrix(0)

    ## Warmtenet: alleen MT-warmtenet instellen, de overige temperatuurniveaus op 0
    warmtenet_mt_share_target = slider_warmtenet / number_of_buildings_present * 100.0
    warmtenet_ht_share_target = var.Matrix(0)
    warmtenet_lt_share_target = var.Matrix(0)

    ## Overige oplossingen: stel in op 0
    lwp_gas_share_target = var.Matrix(0)
    cv_waterstof_share_target = var.Matrix(0)
    houtpellet_share_target = var.Matrix(0)

    ## CV-ketels: alleen daadwerkelijke CV-ketels, gasketels op 0

    ### De share groups in het ETM moeten altijd op precies 100% uitkomen
    ### Pas daarom een correctiefactor toe als (door afronding) de overige drie categorieën op >100% uitkomen
    total_share_target_excluding_cv = (
        lwp_share_target
        + bwp_share_target
        + hybride_gas_share_target
        + warmtenet_mt_share_target
    )

    if any(total_share_target_excluding_cv > 100):
        # Definieer eerst de terugvaloptie voor cv_share_target
        cv_share_target = 100.0 - total_share_target_excluding_cv

        correction_required = True
        correction_factor = total_share_target_excluding_cv / 100.0

        ### Rond de nieuwe target shares naar beneden af op 1 decimaal
        lwp_share_target_corrected = (
            floor(lwp_share_target / correction_factor * 10.0) / 10.0
        )
        bwp_share_target_corrected = (
            floor(bwp_share_target / correction_factor * 10.0) / 10.0
        )
        hybride_gas_share_target_corrected = (
            floor(hybride_gas_share_target / correction_factor * 10.0) / 10.0
        )
        warmtenet_mt_share_target_corrected = (
            floor(warmtenet_mt_share_target / correction_factor * 10.0) / 10.0
        )

        ### Door floor kan er alsnog een verschil met 100% ontstaan zijn.
        ### Bereken daarom het verschil dat aan CV-ketels toegewezen moet worden
        remnant = 100.0 - (
            lwp_share_target_corrected
            + bwp_share_target_corrected
            + hybride_gas_share_target_corrected
            + warmtenet_mt_share_target_corrected
        )
    else:
        correction_required = False

    if correction_required:
        # Voer bovenstaande normalisatie alleen uit in gemeenten waar dit daadwerkelijk moet
        correction_mask = (total_share_target_excluding_cv > 100).mask
        lwp_share_target = (
            lwp_share_target_corrected * correction_mask
        ) | lwp_share_target
        bwp_share_target = (
            bwp_share_target_corrected * correction_mask
        ) | bwp_share_target
        hybride_gas_share_target = (
            hybride_gas_share_target_corrected * correction_mask
        ) | hybride_gas_share_target
        warmtenet_mt_share_target = (
            warmtenet_mt_share_target_corrected * correction_mask
        ) | warmtenet_mt_share_target
        cv_share_target = (remnant * correction_mask) | cv_share_target
    else:
        cv_share_target = 100.0 - total_share_target_excluding_cv

    # Only apply changes in the municipalities where changes are made
    is_changed = (slider_all_e | slider_hybride | slider_warmtenet).mask

    return {
        cv_share: cv_share_target * is_changed,
        cv_waterstof_share: cv_waterstof_share_target * is_changed,
        warmtenet_ht_share: warmtenet_ht_share_target * is_changed,
        warmtenet_mt_share: warmtenet_mt_share_target * is_changed,
        warmtenet_lt_share: warmtenet_lt_share_target * is_changed,
        lwp_gas_share: lwp_gas_share_target * is_changed,
        lwp_share: lwp_share_target * is_changed,
        hybride_gas_share: hybride_gas_share_target * is_changed,
        hybride_waterstof_share: hybride_waterstof_share_target * is_changed,
        bwp_share: bwp_share_target * is_changed,
        aquathermie_share: aquathermie_share_target * is_changed,
        e_boiler_share: e_boiler_share_target * is_changed,
        houtpellet_share: houtpellet_share_target * is_changed,
    }
