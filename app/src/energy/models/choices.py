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
    REG = "REG", "Regio-indeling ZH"
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
    PV28 = "PV28", "Zuid-Holland"


class ResRegionIDs(models.TextChoices):
    ES17 = "ES17", "Alblasserwaard"
    ES23 = "ES23", "Rotterdam Den Haag"
    ES21 = "ES21", "Holland Rijnland"
    ES22 = "ES22", "Midden-Holland"
    ES20 = "ES20", "Hoeksche Waard"
    ES18 = "ES18", "Drechtsteden"
    ES19 = "ES19", "Goeree-Overflakkee"


class RegionIDs(models.TextChoices):
    REG01 = "REG01", "Holland Rijnland"
    REG02 = "REG02", "Midden-Holland"
    REG03 = "REG03", "Drechsteden"
    REG04 = "REG04", "Rotterdam"
    REG05 = "REG05", "Haaglanden"
    REG06 = "REG06", "Zuid-Hollandse Eilanden"


class MunicipalityIDs(models.TextChoices):
    GM0482 = "GM0482", "Alblasserdam"
    GM0484 = "GM0484", "Alphen aan den Rijn"
    GM0489 = "GM0489", "Barendrecht"
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
    GM1525 = "GM1525", "Teylingen"
    GM1621 = "GM1621", "Lansingerland"
    GM1783 = "GM1783", "Westland"
    GM1842 = "GM1842", "Midden-Delfland"
    GM1884 = "GM1884", "Kaag en Braassem"
    GM1892 = "GM1892", "Zuidplas"
    GM1901 = "GM1901", "Bodegraven-Reeuwijk"
    GM1916 = "GM1916", "Leidschendam-Voorburg"
    GM1924 = "GM1924", "Goeree-Overflakkee"
    GM1926 = "GM1926", "Pijnacker-Nootdorp"
    GM1930 = "GM1930", "Nissewaard"
    GM1931 = "GM1931", "Krimpenerwaard"
    GM1963 = "GM1963", "Hoeksche Waard"
    GM1978 = "GM1978", "Molenlanden"
