from typing import Any, Iterable


area_div = {
    "PROV": "Provincie",
    "REG": "Regio-indeling ZH",
    "GM": "Gemeente",
    "RES": "RES-regio's",
    "HSMS": "Netvlakken",
}
provinces = {
    "PV28": "Zuid-Holland",
}
res_regions = {
    "ES17": "Alblasserwaard",
    "ES23": "Rotterdam Den Haag",
    "ES21": "Holland Rijnland",
    "ES22": "Midden-Holland",
    "ES20": "Hoeksche Waard",
    "ES18": "Drechtsteden",
    "ES19": "Goeree-Overflakkee",
}
pzh_regions = {
    "REG01": "Holland Rijnland",
    "REG02": "Midden-Holland",
    "REG03": "Drechsteden",
    "REG04": "Rotterdam",
    "REG05": "Haaglanden",
    "REG06": "Zuid-Hollandse Eilanden",
}
pzh_municipalities = {
    "GM0482": "Alblasserdam",
    "GM0484": "Alphen aan den Rijn",
    "GM0489": "Barendrecht",
    "GM0501": "Brielle",
    "GM0502": "Capelle aan den IJssel",
    "GM0503": "Delft",
    "GM0505": "Dordrecht",
    "GM0512": "Gorinchem",
    "GM0513": "Gouda",
    "GM0518": "'s-Gravenhage'",
    "GM0523": "Hardinxveld-Giessendam",
    "GM0530": "Hellevoetsluis",
    "GM0531": "Hendrik-Ido-Ambacht",
    "GM0534": "Hillegom",
    "GM0537": "Katwijk",
    "GM0542": "Krimpen aan den IJssel",
    "GM0546": "Leiden",
    "GM0547": "Leiderdorp",
    "GM0553": "Lisse",
    "GM0556": "Maassluis",
    "GM0569": "Nieuwkoop",
    "GM0575": "Noordwijk",
    "GM0579": "Oegstgeest",
    "GM0590": "Papendrecht",
    "GM0597": "Ridderkerk",
    "GM0599": "Rotterdam",
    "GM0603": "Rijswijk",
    "GM0606": "Schiedam",
    "GM0610": "Sliedrecht",
    "GM0613": "Albrandswaard",
    "GM0614": "Westvoorne",
    "GM0622": "Vlaardingen",
    "GM0626": "Voorschoten",
    "GM0627": "Waddinxveen",
    "GM0629": "Wassenaar",
    "GM0637": "Zoetermeer",
    "GM0638": "Zoeterwoude",
    "GM0642": "Zwijndrecht",
    "GM1525": "Teylingen",
    "GM1621": "Lansingerland",
    "GM1783": "Westland",
    "GM1842": "Midden-Delfland",
    "GM1884": "Kaag en Braassem",
    "GM1892": "Zuidplas",
    "GM1901": "Bodegraven-Reeuwijk",
    "GM1916": "Leidschendam-Voorburg",
    "GM1924": "Goeree-Overflakkee",
    "GM1926": "Pijnacker-Nootdorp",
    "GM1930": "Nissewaard",
    "GM1931": "Krimpenerwaard",
    "GM1963": "Hoeksche Waard",
    "GM1978": "Molenlanden",
}

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
        if id in carriers:
            return carriers[id]
        raise KeyError(f"Unknown id: {id}")

    if isinstance(id, list):
        return [_get(i) for i in id]
    else:
        return _get(id)
