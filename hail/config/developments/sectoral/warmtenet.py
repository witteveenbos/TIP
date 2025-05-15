from hail.development import AbstractDevelopment
from hail.models.enums import DevelomentType
from typing import TYPE_CHECKING
from config.developments.sectoral._groups import nieuwbouwprojecten
from config.developments.shared import (
    set_heat_sliders_households,
    nieuwbouw_warmtenet_default,
)

if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class Warmtenet(AbstractDevelopment):

    name = "Warmtenet"
    key = "warmtenet"
    unit = "#"
    dev_type = DevelomentType.SECTORAL
    group = nieuwbouwprojecten

    @staticmethod
    def min(var: "Var"):
        return var.Matrix(0)

    @staticmethod
    def max(var: "Var"):
        # De tool kan maximaal de totale bestaande woningvoorraad aan nieuwbouwhuizen per oplossing toevoegen

        number_of_homes_total = var.gqueries.number_of_residences.present

        return number_of_homes_total

    @staticmethod
    def default(var: "Var"):
        return nieuwbouw_warmtenet_default(var)

    @staticmethod
    def sets_ETM_value(var: "Var"):
        return set_heat_sliders_households(var)

    @classmethod
    def aggregate(cls, var: "Var"):
        return var.ui.warmtenet | cls.default(var)
