from __future__ import annotations
from enum import Enum


class DemandSupplyEnum(Enum):
    DEMAND = "demand"
    SUPPLY = "supply"


class CarrierEnum(Enum):
    ALL = "all"
    ELECTRICITY = "electricity"
    GAS = "gas"
    HEAT = "heat"


class BalanceEnum(Enum):
    BALANCE = "balance"
    DEMAND = "demand"
    SUPPLY = "supply"


class EnergyTypeEnum(Enum):
    CURTAILMENT = "Curtailment"
    DEMAND = "Demand"
    PROCESS_FLEX = "Process_flex"
    SUPPLY = "Supply"
    SYSTEM_FLEX = "System_flex"
    EXCHANGE = "Exchange"


class DevelomentType(Enum):
    SECTORAL = "sectoral"
    CONTINUOUS = "continuous"


class AggregationLevel(Enum):
    RES = "res"
    PMIEK = "pmiek"
    PROV = "prov"
    GEM = "gem"
    HSMS = "hsms"


class ResultTypes(Enum):
    MAP = "map"
    NUMBER = "number"
    GRAPH = "graph"


class plotTypes(Enum):
    line = "line"
    bar = "bar"
    scatter = "scatter"


class AreaDivisionEnum(Enum):
    PROV = "PROV"
    REG = "REG"
    GM = "GM"
    RES = "RES"
    HSMS = "HSMS"


class ProvinceIDs(Enum):
    PV28 = "PV28"
    PV27 = "PV27"


class ResRegionIDs(Enum):
    ES17 = "ES17" # Zuid-Holland
    ES23 = "ES23" # Zuid-Holland
    ES21 = "ES21" # Zuid-Holland
    ES22 = "ES22" # Zuid-Holland
    ES20 = "ES20" # Zuid-Holland
    ES18 = "ES18" # Zuid-Holland
    ES19 = "ES19" # Zuid-Holland
    ET1501 = "ET1501"  # Noord-Holland
    ET1502 = "ET1502"  # Noord-Holland
    ET1503 = "ET1503"  # Noord-Holland
    ET1601 = "ET1601"  # Noord-Holland
    ET1602 = "ET1602"  # Noord-Holland
    ET1603 = "ET1603"  # Noord-Holland
    ET1604 = "ET1604"  # Noord-Holland
    ET1605 = "ET1605"  # Noord-Holland
    ET1606 = "ET1606"  # Noord-Holland

class RegionIDs(Enum):
    REG01 = "REG01"
    REG02 = "REG02"
    REG03 = "REG03"
    REG04 = "REG04"
    REG05 = "REG05"
    REG06 = "REG06"
    ET1501 = "ET1501"  # Noord-Holland
    ET1502 = "ET1502"  # Noord-Holland
    ET1503 = "ET1503"  # Noord-Holland
    ET1601 = "ET1601"  # Noord-Holland
    ET1602 = "ET1602"  # Noord-Holland
    ET1603 = "ET1603"  # Noord-Holland
    ET1604 = "ET1604"  # Noord-Holland
    ET1605 = "ET1605"  # Noord-Holland
    ET1606 = "ET1606"  # Noord-Holland


class MunicipalityIDs(Enum):
    GM0358 = "GM0358"  # Aalsmeer
    GM0361 = "GM0361"  # Alkmaar
    GM0362 = "GM0362"  # Amstelveen
    GM0363 = "GM0363"  # Amsterdam
    GM0370 = "GM0370"  # Beemster
    GM0373 = "GM0373"  # Bergen (NH.)
    GM0375 = "GM0375"  # Beverwijk
    GM0376 = "GM0376"  # Blaricum
    GM0377 = "GM0377"  # Bloemendaal
    GM0383 = "GM0383"  # Castricum
    GM0384 = "GM0384"  # Diemen
    GM0385 = "GM0385"  # Edam-Volendam
    GM0388 = "GM0388"  # Enkhuizen
    GM0392 = "GM0392"  # Haarlem
    GM0394 = "GM0394"  # Haarlemmermeer
    GM0396 = "GM0396"  # Heemskerk
    GM0397 = "GM0397"  # Heemstede
    GM0398 = "GM0398"  # Heerhugowaard
    GM0399 = "GM0399"  # Heiloo
    GM0400 = "GM0400"  # Den Helder
    GM0402 = "GM0402"  # Hilversum
    GM0405 = "GM0405"  # Hoorn
    GM0406 = "GM0406"  # Huizen
    GM0415 = "GM0415"  # Landsmeer
    GM0416 = "GM0416"  # Langedijk
    GM0417 = "GM0417"  # Laren
    GM0420 = "GM0420"  # Medemblik
    GM0431 = "GM0431"  # Oostzaan
    GM0432 = "GM0432"  # Opmeer
    GM0437 = "GM0437"  # Ouder-Amstel
    GM0439 = "GM0439"  # Purmerend
    GM0441 = "GM0441"  # Schagen
    GM0448 = "GM0448"  # Texel
    GM0450 = "GM0450"  # Uitgeest
    GM0451 = "GM0451"  # Uithoorn
    GM0453 = "GM0453"  # Velsen
    GM0457 = "GM0457"  # Weesp
    GM0473 = "GM0473"  # Zandvoort
    GM0479 = "GM0479"  # Zaanstad
    GM0482 = "GM0482"
    GM0484 = "GM0484"
    GM0489 = "GM0489"
    GM0498 = "GM0498"  # Drechterland
    GM0501 = "GM0501"
    GM0502 = "GM0502"
    GM0503 = "GM0503"
    GM0505 = "GM0505"
    GM0512 = "GM0512"
    GM0513 = "GM0513"
    GM0518 = "GM0518"
    GM0523 = "GM0523"
    GM0530 = "GM0530"
    GM0531 = "GM0531"
    GM0532 = "GM0532"  # Stede Broec
    GM0534 = "GM0534"
    GM0537 = "GM0537"
    GM0542 = "GM0542"
    GM0546 = "GM0546"
    GM0547 = "GM0547"
    GM0553 = "GM0553"
    GM0556 = "GM0556"
    GM0569 = "GM0569"
    GM0575 = "GM0575"
    GM0579 = "GM0579"
    GM0590 = "GM0590"
    GM0597 = "GM0597"
    GM0599 = "GM0599"
    GM0603 = "GM0603"
    GM0606 = "GM0606"
    GM0610 = "GM0610"
    GM0613 = "GM0613"
    GM0614 = "GM0614"
    GM0622 = "GM0622"
    GM0626 = "GM0626"
    GM0627 = "GM0627"
    GM0629 = "GM0629"
    GM0637 = "GM0637"
    GM0638 = "GM0638"
    GM0642 = "GM0642"
    GM0852 = "GM0852"  # Waterland
    GM0880 = "GM0880"  # Wormerland
    GM1525 = "GM1525"
    GM1598 = "GM1598"  # Koggenland
    GM1621 = "GM1621"
    GM1696 = "GM1696"  # Wijdemeren
    GM1783 = "GM1783"
    GM1842 = "GM1842"
    GM1884 = "GM1884"
    GM1892 = "GM1892"
    GM1901 = "GM1901"
    GM1911 = "GM1911"  # Hollands Kroon
    GM1916 = "GM1916"
    GM1924 = "GM1924"
    GM1926 = "GM1926"
    GM1930 = "GM1930"
    GM1931 = "GM1931"
    GM1942 = "GM1942"  # Gooise Meren
    GM1963 = "GM1963"
    GM1978 = "GM1978"
    GM1980 = "GM1980"  # Dijk en Waard


class HSMSIDs(Enum):
    MOERDIJK = "Moerdijk"
    OOLTGENSPLAAT_50_KV = "OOLTGENSPLAAT 50 kV"
    KLAASWAAL_50_KV = "Klaaswaal 50 kV"
    DORDRECHT_STERRENBURG_50_KV = "Dordrecht Sterrenburg 50 kV"
    BIESBOSCH = "Biesbosch"
    S_GRAVENDEEL_50_KV = "s Gravendeel 50 kV"
    MIDDELHARNIS_50_KV = "Middelharnis 50 kV"
    WALBURG_50_KV_50_KV = "Walburg 50 kV 50 kV"
    DORDRECHT_MERWEDEHAVEN_50_KV = "Dordrecht Merwedehaven 50 kV"
    GEERVLIET_25_KV = "Geervliet 25 kV"
    ROTTERDAM_OUDELAND_25_KV = "Rotterdam Oudeland 25 kV"
    HOOGVLIET_25_KV = "Hoogvliet 25 kV"
    ALBLASSERWAARD_WEST_50_KV = "Alblasserwaard West 50 kV"
    BOTLEK_25_KV = "Botlek 25 kV"
    VONDELINGENWEG_66_KV = "Vondelingenweg 66 kV"
    SLIKKERVEER_50_KV = "Slikkerveer 50 kV"
    ROTTERDAM_WAALHAVEN_25_KV = "Rotterdam Waalhaven 25 kV"
    THEEMSWEG_25_KV = "Theemsweg 25 kV"
    ROTTERDAM_DOKLAAN_25_KV = "Rotterdam Doklaan 25 kV"
    ARKEL_50_KV = "Arkel 50 kV"
    GERBRANDYWEG_25_KV = "Gerbrandyweg 25 kV"
    ROTTERDAM_BENJ_FRANKLINKLINSTRAAT_25_KV = "Rotterdam Benj Franklinklinstraat 25 kV"
    ZAMENHOFSTRAAT_25KV = "Zamenhofstraat 25kV"
    KRIMPEN_LANGELAND_50_KV = "Krimpen_Langeland 50 kV"
    HOOFDWEG_25_KV = "Hoofdweg 25 kV"
    EUROPOORT_25_KV = "Europoort 25 kV"
    ID_33002 = "33002"
    SCHIEBROEK_25_KV = "Schiebroek 25 kV"
    GRINDWEG_25_KV = "Grindweg 25 kV"
    ROTTERDAM_OMMOORD_25_KV = "Rotterdam Ommoord 25 kV"
    ID_35009 = "35009"
    ID_44007 = "44007"
    ID_33063 = "33063"
    DELFT_1_25_KV = "Delft 1 25 kV"
    ID_44276 = "44276"
    ID_44130 = "44130"
    ID_46004 = "46004"
    ID_44140 = "44140"
    GOUDA_IJSSELDIJK_50_KV = "Gouda Ijsseldijk 50 kV"
    ID_43126 = "43126"
    MAASVLAKTE_66_66_KV = "Maasvlakte 66 66 kV"
    ID_46003 = "46003"
    ID_45004 = "45004"
    ID_43003 = "43003"
    ID_43027 = "43027"
    OS_ZEVENHUIZEN = "OS ZEVENHUIZEN"
    DEN_HAAG_HVS_ZUID_25_KV = "Den Haag HVS Zuid 25 kV"
    ZOETERMEER_9_25_KV = "Zoetermeer 9 25 kV"
    DELFT_2_25_KV = "Delft 2 25 kV"
    ZOETERMEER_10_25_KV = "Zoetermeer 10 25 kV"
    DEN_HAAG_HVS_YPENBURG_25_KV = "Den Haag HVS_Ypenburg 25 kV"
    HENGELOLAAN_25_KV = "Hengelolaan 25 kV"
    DEN_HAAG_HVS_CENTRALE_25_KV = "Den Haag HVS Centrale 25 kV"
    DEN_HAAG_HVS_OOST_25_KV = "Den Haag HVS Oost 25 kV"
    OS_ALPHEN_CENTRUM = "OS ALPHEN CENTRUM"
    OS_ALPHEN_WEST = "OS ALPHEN WEST"
    OS_ZOETERWOUDE = "OS ZOETERWOUDE"
    OS_WASSENAAR = "OS WASSENAAR"
    OS_LEIDEN_ZUID_WEST = "OS LEIDEN ZUID-WEST"
    OS_LEIDERDORP = "OS LEIDERDORP"
    OS_LEIDEN_NOORD = "OS LEIDEN NOORD"
    OS_RIJKSUNIVERSITEIT_LEIDEN = "OS RIJKSUNIVERSITEIT LEIDEN"
    OS_NIEUWKOOP = "OS NIEUWKOOP"
    OS_RIJNSBURG = "OS RIJNSBURG"
    OS_KATWIJK = "OS KATWIJK"
    OS_LEIMUIDEN = "OS LEIMUIDEN"
    OS_SASSENHEIM = "OS SASSENHEIM"
    OS_NOORDWIJK = "OS NOORDWIJK"
    OS_LISSE = "OS LISSE"
    OS_HILLEGOM = "OS HILLEGOM"
    OS_UITHOORN = "OS UITHOORN"
    OS_AALSMEER_BLOEMENVEILING = "OS AALSMEER BLOEMENVEILING"
    OS_HAARLEMMERMEER = "OS HAARLEMMERMEER"
    OS_HUIZEN = "OS HUIZEN"
    BREUKELEN_50_KV = "Breukelen 50 kV"
    OS_HILVERSUM_RAAFSTRAAT = "OS HILVERSUM RAAFSTRAAT"
    OS_HILVERSUM_JONKERWEG = "OS HILVERSUM JONKERWEG"
    OS_HILVERSUM_NOORDER_BEGRAAFP = "OS HILVERSUM NOORDER BEGRAAFP"
    OS_S_GRAVELAND = "OS 'S-GRAVELAND"
    OS_NIEUW_VENNEP = "OS NIEUW VENNEP"
    OS_ROZENBURG = "OS ROZENBURG"
    OS_SCHIPHOL_OOST = "OS SCHIPHOL OOST"
    OS_HOOFDDORP = "OS HOOFDDORP"
    OS_NIEUWE_MEER = "OS NIEUWE MEER"
    OS_HILVERSUM_CRAILO_PROV = "OS HILVERSUM CRAILO PROV."
    OS_BIJLMER_ZUID = "OS BIJLMER ZUID"
    OS_AMSTELVEEN = "OS AMSTELVEEN"
    OS_WEESP = "OS WEESP"
    OS_NAARDEN = "OS NAARDEN"
    OS_AMSTELVEEN_BOLWERK = "OS AMSTELVEEN BOLWERK"
    OS_BIJLMER_NOORD = "OS BIJLMER NOORD"
    OS_VENSERWEG = "OS VENSERWEG"
    OS_ZORGVLIED = "OS ZORGVLIED"
    OS_KARPERWEG = "OS KARPERWEG"
    OS_RHIJNSPOOR = "OS RHIJNSPOOR"
    OS_HOOGTE_KADIJK = "OS HOOGTE KADIJK"
    OS_WATERGRAAFSMEER = "OS WATERGRAAFSMEER"
    OS_MARNIXSTRAAT = "OS MARNIXSTRAAT"
    OS_IJBURG = "OS IJBURG"
    OS_WESTZAANSTRAAT = "OS WESTZAANSTRAAT"
    OS_VLIEGENBOS = "OS VLIEGENBOS"
    OS_SCHALKWIJK = "OS SCHALKWIJK"
    OS_SCHIPLUIDENLAAN = "OS SCHIPLUIDENLAAN"
    OS_HAARLEM_WEST = "OS HAARLEM WEST"
    OS_VIJFHUIZEN = "OS VIJFHUIZEN"
    OS_SLOTERMEER = "OS SLOTERMEER"
    OS_BASISWEG = "OS BASISWEG"
    OS_OVERVEEN = "OS OVERVEEN"
    OS_WAARDERPOLDER = "OS WAARDERPOLDER"
    OS_RUIGOORD = "OS RUIGOORD"
    OS_IJPOLDER = "OS IJPOLDER"
    OS_ZAANDAM_WEST = "OS ZAANDAM WEST"
    OS_IJMUIDEN = "OS IJMUIDEN"
    OS_ZAANDIJK = "OS ZAANDIJK"
    OS_ZAANDAM_NOORD = "OS ZAANDAM NOORD"
    OS_VELSEN = "OS VELSEN"
    OS_BEVERWIJK = "OS BEVERWIJK"
    OS_KROMMENIE = "OS KROMMENIE"
    OS_WORMERVEER = "OS WORMERVEER"
    OS_UITGEEST = "OS UITGEEST"
    OS_HEILOO = "OS HEILOO"
    OS_WESTHAVEN = "OS WESTHAVEN"
    OS_NOORD_PAPAVERWEG = "OS NOORD PAPAVERWEG"
    OS_EDAM = "OS EDAM"
    OS_PURMEREND_SCHAEPMANSTRAAT = "OS PURMEREND SCHAEPMANSTRAAT"
    OS_PURMEREND_KWADIJKERKOOGWEG = "OS PURMEREND KWADIJKERKOOGWEG"
    OS_OTERLEEK = "OS OTERLEEK"
    OS_HOORN_HOLENWEG = "OS HOORN HOLENWEG"
    OS_HOORN_GELDELOZEWEG = "OS HOORN GELDELOZEWEG"
    OS_HEERHUGOWAARD = "OS HEERHUGOWAARD"
    OS_WESTWOUD = "OS WESTWOUD"
    OS_OUDORP = "OS OUDORP"
    OS_ALKMAAR = "OS ALKMAAR"
    OS_WARMENHUIZEN = "OS WARMENHUIZEN"
    OS_SCHAGEN = "OS SCHAGEN"
    OS_ANNA_PAULOWNA = "OS ANNA PAULOWNA"
    OS_DEN_HELDER_DE_SCHOOTEN = "OS DEN HELDER DE SCHOOTEN"
    OS_DEN_HELDER_VOGELWIJK = "OS DEN HELDER VOGELWIJK"
    OS_HOOGWOUD = "OS HOOGWOUD"
    OS_DE_WEEL = "OS DE WEEL"
    OS_WERVERSHOOF = "OS WERVERSHOOF"
    OS_MIDDENMEER = "OS MIDDENMEER"
    OS_MEDEMBLIK = "OS MEDEMBLIK"
    OS_ULKESLUIS = "OS ULKESLUIS"
    OS_TEXEL = "OS TEXEL"
    OS_ENKHUIZEN = "OS ENKHUIZEN"


AllAreaDivisionIDs = ProvinceIDs | ResRegionIDs | RegionIDs | MunicipalityIDs | HSMSIDs


class MainScenarioEnum(Enum):
    # II3050_DEC_NL2019_CY2012_2040 = "ii3050_dec_nl2019_cy2012_2040"
    # II3050_EUR_NL2019_CY2012_2040 = "ii3050_eur_nl2019_cy2012_2040"
    # II3050_INT_NL2019_CY2012_2040 = "ii3050_int_nl2019_cy2012_2040"
    # II3050_NAT_NL2019_CY2012_2040 = "ii3050_nat_nl2019_cy2012_2040"
    # II3050_DEC_NL2019_CY2012_2050 = "ii3050_dec_nl2019_cy2012_2050"
    # II3050_EUR_NL2019_CY2012_2050 = "ii3050_eur_nl2019_cy2012_2050"
    # II3050_INT_NL2019_CY2012_2050 = "ii3050_int_nl2019_cy2012_2050"
    # II3050_NAT_NL2019_CY2012_2050 = "ii3050_nat_nl2019_cy2012_2050"
    II3050_KM_NL2019_CY2012_2040 = "ii3050_km_nl2019_cy2012_2040"
    II3050_EV_NL2019_CY2012_2040 = "ii3050_ev_nl2019_cy2012_2040"
    II3050_GB_NL2019_CY2012_2040 = "ii3050_gb_nl2019_cy2012_2040"
    II3050_HA_NL2019_CY2012_2040 = "ii3050_ha_nl2019_cy2012_2040"
    II3050_KM_NL2019_CY2012_2050 = "ii3050_km_nl2019_cy2012_2050"
    II3050_EV_NL2019_CY2012_2050 = "ii3050_ev_nl2019_cy2012_2050"
    II3050_GB_NL2019_CY2012_2050 = "ii3050_gb_nl2019_cy2012_2050"
    II3050_HA_NL2019_CY2012_2050 = "ii3050_ha_nl2019_cy2012_2050"
