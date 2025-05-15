from typing import TYPE_CHECKING
from hail.development import AbstractDevelopment
from hail.models.matrix import Matrix

if TYPE_CHECKING:
    from hail.context import ContextProvider

    Var = ContextProvider


class TestDevelopment1(AbstractDevelopment):
    group = "Test Group"
    key = "test_dev1"
    name = "Test Development"
    unit = "test_unit"
    dev_type = "test_dev_type"

    @property
    def max(var: "Var"):
        return var.Matrix(10)

    @property
    def min(var: "Var"):
        return var.Matrix(1)

    @property
    def default(var: "Var"):
        return var.Matrix(5)

    @property
    def sets_ETM_value(var: "Var"):
        raise NotImplementedError

    @property
    def aggregate(var: "Var"):
        raise NotImplementedError


class TestDevelopment2(AbstractDevelopment):
    group = "Test Group"
    key = "test_dev2"
    name = "Test Development"
    unit = "test_unit"
    dev_type = "test_dev_type"

    @property
    def max(var: "Var"):
        return var.Matrix(10)

    @property
    def min(var: "Var"):
        return var.Matrix(1)

    @property
    def default(var: "Var"):
        return var.Matrix(5)

    @property
    def sets_ETM_value(var: "Var"):
        raise NotImplementedError

    @property
    def aggregate(var: "Var"):
        raise NotImplementedError


class TestDevelopment3(AbstractDevelopment):
    group = "Test Group"
    key = "test_dev3"
    name = "Test Development"
    unit = "test_unit"
    dev_type = "test_dev_type"

    @property
    def max(var: "Var"):
        return var.Matrix(10)

    @property
    def min(var: "Var"):
        return var.Matrix(1)

    @property
    def default(var: "Var"):
        return var.Matrix(5)

    @property
    def sets_ETM_value(var: "Var"):
        raise NotImplementedError

    @property
    def aggregate(var: "Var"):
        raise NotImplementedError
