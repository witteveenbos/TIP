from typing import Any, Iterable


area_div = {
    "PROV": "Provincie",
    # "REG": "Regio-indeling ZH", # can this be commented out?
    "GM": "Gemeente",
    "RES": "RES-regio's",
    "HSMS": "Netvlakken",
}
provinces = {
    "PV27": "Noord-Holland",
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
    "ET1501": "Kop van Noord-Holland",
    "ET1502": "Regio Alkmaar",
    "ET1503": "West-Friesland",
    "ET1601": "Amsterdam",
    "ET1602": "IJmond-Zuid-Kennemerland",
    "ET1603": "Zaanstreek-Waterland",
    "ET1604": "Gooi en Vechtstreek",
    "ET1605": "Haarlemmermeer",
    "ET1606": "Amstelland",
}
pzh_regions = {
    "REG01": "Holland Rijnland",
    "REG02": "Midden-Holland",
    "REG03": "Drechsteden",
    "REG04": "Rotterdam",
    "REG05": "Haaglanden",
    "REG06": "Zuid-Hollandse Eilanden",
    "ET1501": "Kop van Noord-Holland",
    "ET1502": "Regio Alkmaar",
    "ET1503": "West-Friesland",
    "ET1601": "Amsterdam",
    "ET1602": "IJmond-Zuid-Kennemerland",
    "ET1603": "Zaanstreek-Waterland",
    "ET1604": "Gooi en Vechtstreek",
    "ET1605": "Haarlemmermeer",
    "ET1606": "Amstelland",
}
pzh_municipalities = {
    "GM0358": "Aalsmeer",
    "GM0361": "Alkmaar",
    "GM0362": "Amstelveen",
    "GM0363": "Amsterdam",
    "GM0370": "Beemster",
    "GM0373": "Bergen (NH.)",
    "GM0375": "Beverwijk",
    "GM0376": "Blaricum",
    "GM0377": "Bloemendaal",
    "GM0383": "Castricum",
    "GM0384": "Diemen",
    "GM0385": "Edam-Volendam",
    "GM0388": "Enkhuizen",
    "GM0392": "Haarlem",
    "GM0394": "Haarlemmermeer",
    "GM0396": "Heemskerk",
    "GM0397": "Heemstede",
    "GM0398": "Heerhugowaard",
    "GM0399": "Heiloo",
    "GM0400": "Den Helder",
    "GM0402": "Hilversum",
    "GM0405": "Hoorn",
    "GM0406": "Huizen",
    "GM0415": "Landsmeer",
    "GM0416": "Langedijk",
    "GM0417": "Laren",
    "GM0420": "Medemblik",
    "GM0431": "Oostzaan",
    "GM0432": "Opmeer",
    "GM0437": "Ouder-Amstel",
    "GM0439": "Purmerend",
    "GM0441": "Schagen",
    "GM0448": "Texel",
    "GM0450": "Uitgeest",
    "GM0451": "Uithoorn",
    "GM0453": "Velsen",
    "GM0457": "Weesp",
    "GM0473": "Zandvoort",
    "GM0479": "Zaanstad",
    "GM0482": "Alblasserdam",
    "GM0484": "Alphen aan den Rijn",
    "GM0489": "Barendrecht",
    "GM0498": "Drechterland",
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
    "GM0532": "Stede Broec",
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
    "GM0852": "Waterland",
    "GM0880": "Wormerland",
    "GM1525": "Teylingen",
    "GM1598": "Koggenland",
    "GM1621": "Lansingerland",
    "GM1696": "Wijdemeren",
    "GM1783": "Westland",
    "GM1842": "Midden-Delfland",
    "GM1884": "Kaag en Braassem",
    "GM1892": "Zuidplas",
    "GM1901": "Bodegraven-Reeuwijk",
    "GM1911": "Hollands Kroon",
    "GM1916": "Leidschendam-Voorburg",
    "GM1924": "Goeree-Overflakkee",
    "GM1926": "Pijnacker-Nootdorp",
    "GM1930": "Nissewaard",
    "GM1931": "Krimpenerwaard",
    "GM1942": "Gooise Meren",
    "GM1963": "Hoeksche Waard",
    "GM1978": "Molenlanden",
    "GM1980": "Dijk en Waard",
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
