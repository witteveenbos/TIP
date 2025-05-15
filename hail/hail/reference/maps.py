from enum import Enum


class MapTypes(Enum):

    ALL_CARRIERS_BALANCE_NORMALIZED = "all_carriers_balance_normalized"
    ALL_CARRIERS_DEMAND = "all_carriers_demand"
    ALL_CARRIERS_SUPPLY = "all_carriers_supply"
    ELECTRICITY_BALANCE_NORMALIZED = "electricity_balance_normalized"
    ELECTRICITY_DEMAND = "electricity_demand"
    ELECTRICITY_SUPPLY = "electricity_supply"
    GAS_BALANCE_NORMALIZED = "gas_balance_normalized"
    GAS_DEMAND = "gas_demand"
    GAS_SUPPLY = "gas_supply"
    GRID_LOAD_DEMAND = "grid_load_demand"
    GRID_LOAD_SUPPY = "grid_load_suppy"
    HEAT_BALANCE_NORMALIZED = "heat_balance_normalized"
    HEAT_DEMAND = "heat_demand"
    HEAT_SUPPLY = "heat_supply"
