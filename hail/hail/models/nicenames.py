from hail.models.enums import (
    HSMSIDs,
    MunicipalityIDs,
    ProvinceIDs,
    RegionIDs,
    ResRegionIDs,
)

area_div = {
    "PROV": "Provincie",
    "REG": "Regio-indeling NH",  # can this be commented out? > No
    "GM": "Gemeente",
    "RES": "RES-regio's",
    "HSMS": "Netvlakken",
}
provinces = {
    ProvinceIDs.PV20.value: "Groningen",
    ProvinceIDs.PV22.value: "Drenthe",
    ProvinceIDs.PV23.value: "Overijssel",
}
res_regions = {
    ResRegionIDs.ET0101.value: "Groningen",
    ResRegionIDs.ET0301.value: "Drenthe",
    ResRegionIDs.ET0501.value: "West-Overijssel",
}
pzh_regions = {
    RegionIDs.REGET0101.value: "Groningen",
    RegionIDs.REGET0301.value: "Drenthe",
    RegionIDs.REGET0501.value: "West-Overijssel",
}
pzh_municipalities = {
    MunicipalityIDs.GM1680.value: "Aa en Hunze",
    MunicipalityIDs.GM0106.value: "Assen",
    MunicipalityIDs.GM1681.value: "Borger-Odoorn",
    MunicipalityIDs.GM0109.value: "Coevorden",
    MunicipalityIDs.GM1690.value: "De Wolden",
    MunicipalityIDs.GM1979.value: "Eemsdelta",
    MunicipalityIDs.GM0114.value: "Emmen",
    MunicipalityIDs.GM0014.value: "Groningen",
    MunicipalityIDs.GM1966.value: "Het Hogeland",
    MunicipalityIDs.GM0118.value: "Hoogeveen",
    MunicipalityIDs.GM0119.value: "Meppel",
    MunicipalityIDs.GM1731.value: "Midden-Drenthe",
    MunicipalityIDs.GM1952.value: "Midden-Groningen",
    MunicipalityIDs.GM1699.value: "Noordenveld",
    MunicipalityIDs.GM1895.value: "Oldambt",
    MunicipalityIDs.GM0765.value: "Pekela",
    MunicipalityIDs.GM0037.value: "Stadskanaal",
    MunicipalityIDs.GM1730.value: "Tynaarlo",
    MunicipalityIDs.GM0047.value: "Veendam",
    MunicipalityIDs.GM1969.value: "Westerkwartier",
    MunicipalityIDs.GM1701.value: "Westerveld",
    MunicipalityIDs.GM1950.value: "Westerwolde",
    MunicipalityIDs.GM1708.value: "Steenwijkerland",
    MunicipalityIDs.GM0180.value: "Staphorst",
    MunicipalityIDs.GM0160.value: "Hardenberg",
}

hsms = {hsms_id.value: hsms_id.value for hsms_id in HSMSIDs}

carriers = {
    "Electricity": "Electriciteit",
    "Hydrogen": "Waterstof",
    "Methane": "Methaan",
}


def nicify(id: str | list[str]) -> str | list[str]:

    def _get(id: str) -> str:
        if id in area_div:
            return area_div[id]
        if id in provinces:
            return provinces[id]
        if id in res_regions:
            return res_regions[id]
        if id in pzh_regions:
            return pzh_regions[id]
        if id in pzh_municipalities:
            return pzh_municipalities[id]
        if id in hsms:
            return hsms[id]
        if id in carriers:
            return carriers[id]
        raise KeyError(f"Unknown id: {id}")

    if isinstance(id, list):
        return [_get(i) for i in id]
    else:
        return _get(id)
