from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from hail.context import ContextProvider


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResult(ABC):

    @property
    @abstractmethod
    def key(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        pass
