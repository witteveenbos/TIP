from pydantic import BaseModel

Value = float | int


class GroupFields(BaseModel):

    all_electric: Value
    besparing_energievraag_verspreide_industrie: Value
    geothermie: Value
    hybride: Value
    oppervlakte_kassen: Value
    reductie_warmtevraag: Value
    utiliteiten_all_electric: Value
    utiliteiten_besparing_warmtevraag: Value
    utiliteiten_hybride: Value
    utiliteiten_warmtenet: Value
    verandering_persoonskilometers: Value
    verandering_vrachtkilometers: Value
    verduurzaming_bestaand_all_electric: Value
    verduurzaming_bestaand_hybride: Value
    verduurzaming_bestaand_warmtenet: Value
    warmtenet: Value
    wind_op_land: Value
    zon_op_dak_grootschalig: Value
    zon_op_dak_huishoudens: Value
    zon_op_veld: Value
