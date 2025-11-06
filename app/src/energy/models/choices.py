from django.db import models


class InputTypes(models.TextChoices):
    SECTORAL = "sectoral"
    CONTINUOUS = "continuous"


class MapTypes(models.TextChoices):
    ENERGY_BALANCE = "energy_balance"


class GraphTypes(models.TextChoices):
    ENERGY_BALANCE_BAR_CHART = "energy_balance_bar_chart"


class AreaDivision(models.TextChoices):
    PROV = "PROV", "Provincie"
    REG = "REG", "Regio-indeling NH" # Can this be commented out? > No
    GM = "GM", "Gemeente"
    RES = "RES", "RES-regio's"
    HSMS = "HSMS", "Netvlakken"

    @property
    def geo_ids(self):
        if self == AreaDivision.PROV:
            return ProvinceIDs.values
        elif self == AreaDivision.REG:
            return RegionIDs.values
        elif self == AreaDivision.GM:
            return MunicipalityIDs.values
        elif self == AreaDivision.RES:
            return ResRegionIDs.values


class ProvinceIDs(models.TextChoices):
    PV27 = "PV27", "Noord-Holland"
    PV28 = "PV28", "Zuid-Holland"


class ResRegionIDs(models.TextChoices):
    ES17 = "ES17", "Alblasserwaard"
    ES23 = "ES23", "Rotterdam Den Haag"
    ES21 = "ES21", "Holland Rijnland"
    ES22 = "ES22", "Midden-Holland"
    ES20 = "ES20", "Hoeksche Waard"
    ES18 = "ES18", "Drechtsteden"
    ES19 = "ES19", "Goeree-Overflakkee"
    ET1501 = "ET1501", "Kop van Noord-Holland"
    ET1502 = "ET1502", "Regio Alkmaar"
    ET1503 = "ET1503", "West-Friesland"
    ET1601 = "ET1601", "Amsterdam"
    ET1602 = "ET1602", "IJmond-Zuid-Kennemerland"
    ET1603 = "ET1603", "Zaanstreek-Waterland"
    ET1604 = "ET1604", "Gooi en Vechtstreek"
    ET1605 = "ET1605", "Haarlemmermeer"
    ET1606 = "ET1606", "Amstelland"


class RegionIDs(models.TextChoices):
    REG01 = "REG01", "Holland Rijnland"
    REG02 = "REG02", "Midden-Holland"
    REG03 = "REG03", "Drechsteden"
    REG04 = "REG04", "Rotterdam"
    REG05 = "REG05", "Haaglanden"
    REG06 = "REG06", "Zuid-Hollandse Eilanden"
    ET1501 = "ET1501", "Kop van Noord-Holland"
    ET1502 = "ET1502", "Regio Alkmaar"
    ET1503 = "ET1503", "West-Friesland"
    ET1601 = "ET1601", "Amsterdam"
    ET1602 = "ET1602", "IJmond-Zuid-Kennemerland"
    ET1603 = "ET1603", "Zaanstreek-Waterland"
    ET1604 = "ET1604", "Gooi en Vechtstreek"
    ET1605 = "ET1605", "Haarlemmermeer"
    ET1606 = "ET1606", "Amstelland"


class MunicipalityIDs(models.TextChoices):
    GM0358 = "GM0358", "Aalsmeer"
    GM0361 = "GM0361", "Alkmaar"
    GM0362 = "GM0362", "Amstelveen"
    GM0363 = "GM0363", "Amsterdam"
    GM0370 = "GM0370", "Beemster"
    GM0373 = "GM0373", "Bergen (NH.)"
    GM0375 = "GM0375", "Beverwijk"
    GM0376 = "GM0376", "Blaricum"
    GM0377 = "GM0377", "Bloemendaal"
    GM0383 = "GM0383", "Castricum"
    GM0384 = "GM0384", "Diemen"
    GM0385 = "GM0385", "Edam-Volendam"
    GM0388 = "GM0388", "Enkhuizen"
    GM0392 = "GM0392", "Haarlem"
    GM0394 = "GM0394", "Haarlemmermeer"
    GM0396 = "GM0396", "Heemskerk"
    GM0397 = "GM0397", "Heemstede"
    GM0398 = "GM0398", "Heerhugowaard"
    GM0399 = "GM0399", "Heiloo"
    GM0400 = "GM0400", "Den Helder"
    GM0402 = "GM0402", "Hilversum"
    GM0405 = "GM0405", "Hoorn"
    GM0406 = "GM0406", "Huizen"
    GM0415 = "GM0415", "Landsmeer"
    GM0416 = "GM0416", "Langedijk"
    GM0417 = "GM0417", "Laren"
    GM0420 = "GM0420", "Medemblik"
    GM0431 = "GM0431", "Oostzaan"
    GM0432 = "GM0432", "Opmeer"
    GM0437 = "GM0437", "Ouder-Amstel"
    GM0439 = "GM0439", "Purmerend"
    GM0441 = "GM0441", "Schagen"
    GM0448 = "GM0448", "Texel"
    GM0450 = "GM0450", "Uitgeest"
    GM0451 = "GM0451", "Uithoorn"
    GM0453 = "GM0453", "Velsen"
    GM0457 = "GM0457", "Weesp"
    GM0473 = "GM0473", "Zandvoort"
    GM0479 = "GM0479", "Zaanstad"
    GM0482 = "GM0482", "Alblasserdam"
    GM0484 = "GM0484", "Alphen aan den Rijn"
    GM0489 = "GM0489", "Barendrecht"
    GM0498 = "GM0498", "Drechterland"
    GM0501 = "GM0501", "Brielle"
    GM0502 = "GM0502", "Capelle aan den IJssel"
    GM0503 = "GM0503", "Delft"
    GM0505 = "GM0505", "Dordrecht"
    GM0512 = "GM0512", "Gorinchem"
    GM0513 = "GM0513", "Gouda"
    GM0518 = "GM0518", "'s-Gravenhage'"
    GM0523 = "GM0523", "Hardinxveld-Giessendam"
    GM0530 = "GM0530", "Hellevoetsluis"
    GM0531 = "GM0531", "Hendrik-Ido-Ambacht"
    GM0532 = "GM0532", "Stede Broec"
    GM0534 = "GM0534", "Hillegom"
    GM0537 = "GM0537", "Katwijk"
    GM0542 = "GM0542", "Krimpen aan den IJssel"
    GM0546 = "GM0546", "Leiden"
    GM0547 = "GM0547", "Leiderdorp"
    GM0553 = "GM0553", "Lisse"
    GM0556 = "GM0556", "Maassluis"
    GM0569 = "GM0569", "Nieuwkoop"
    GM0575 = "GM0575", "Noordwijk"
    GM0579 = "GM0579", "Oegstgeest"
    GM0590 = "GM0590", "Papendrecht"
    GM0597 = "GM0597", "Ridderkerk"
    GM0599 = "GM0599", "Rotterdam"
    GM0603 = "GM0603", "Rijswijk"
    GM0606 = "GM0606", "Schiedam"
    GM0610 = "GM0610", "Sliedrecht"
    GM0613 = "GM0613", "Albrandswaard"
    GM0614 = "GM0614", "Westvoorne"
    GM0622 = "GM0622", "Vlaardingen"
    GM0626 = "GM0626", "Voorschoten"
    GM0627 = "GM0627", "Waddinxveen"
    GM0629 = "GM0629", "Wassenaar"
    GM0637 = "GM0637", "Zoetermeer"
    GM0638 = "GM0638", "Zoeterwoude"
    GM0642 = "GM0642", "Zwijndrecht"
    GM0852 = "GM0852", "Waterland"
    GM0880 = "GM0880", "Wormerland"
    GM1525 = "GM1525", "Teylingen"
    GM1598 = "GM1598", "Koggenland"
    GM1621 = "GM1621", "Lansingerland"
    GM1696 = "GM1696", "Wijdemeren"
    GM1783 = "GM1783", "Westland"
    GM1842 = "GM1842", "Midden-Delfland"
    GM1884 = "GM1884", "Kaag en Braassem"
    GM1892 = "GM1892", "Zuidplas"
    GM1901 = "GM1901", "Bodegraven-Reeuwijk"
    GM1911 = "GM1911", "Hollands Kroon"
    GM1916 = "GM1916", "Leidschendam-Voorburg"
    GM1924 = "GM1924", "Goeree-Overflakkee"
    GM1926 = "GM1926", "Pijnacker-Nootdorp"
    GM1930 = "GM1930", "Nissewaard"
    GM1931 = "GM1931", "Krimpenerwaard"
    GM1942 = "GM1942", "Gooise Meren"
    GM1963 = "GM1963", "Hoeksche Waard"
    GM1978 = "GM1978", "Molenlanden"
    GM1980 = "GM1980", "Dijk en Waard"
