from mock_context import mock_context_provider
import pytest


def test_matrix_init_against_invalid():
    # Create a ContextProvider instance
    var = mock_context_provider

    # this test fail if this does not raise a TypeError
    with pytest.raises(TypeError, match="Value must be an int or float"):
        var.Matrix("1")

    with pytest.raises(TypeError, match="Value must be an int or float"):
        var.Matrix([1, 2, 3])


def test_matrix_init_against_valid():
    var = mock_context_provider

    # these should pass as float and int are valid types
    var.Matrix(1)
    var.Matrix(1.0)
    var.Matrix(None)
