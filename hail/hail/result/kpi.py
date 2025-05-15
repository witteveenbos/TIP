from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from hail.context import ContextProvider
from hail.models.matrix import Matrix
from hail.result.base import AbstractResult


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResultKPI(AbstractResult):

    @property
    @abstractmethod
    def number(self, var: Var) -> Matrix:
        pass

    @property
    @abstractmethod
    def number_aggregate(self, var: Var) -> Matrix:
        pass
