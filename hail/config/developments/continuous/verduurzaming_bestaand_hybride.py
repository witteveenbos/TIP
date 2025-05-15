from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.continuous._groups import verduurzaming_bestaande_bouw
from config.developments.shared import (
    set_heat_sliders_households,
    bestaand_hybride_default,
)

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class VerduurzamingBestaandHybride(AbstractDevelopment):

    name = "Verduurzaming bestaand hybride"
    key = "verduurzaming_bestaand_hybride"
    unit = "#"
    dev_type = DevelomentType.CONTINUOUS
    group = verduurzaming_bestaande_bouw

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # De tool kan maximaal de totale bestaande woningvoorraad per oplossing toevoegen

        number_of_homes_total = var.gqueries.number_of_residences.present

        return number_of_homes_total

    @staticmethod
    def default(var: "Var"):
        return bestaand_hybride_default(var)

    @staticmethod
    def sets_ETM_value(var: "Var"):
        return set_heat_sliders_households(var)

    @classmethod
    def aggregate(cls, var: "Var"):
        return var.ui.verduurzaming_bestaand_hybride | cls.default(var)
