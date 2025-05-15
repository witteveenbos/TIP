import importlib
import logging
from pathlib import Path
import sys
from hail.development import Group
from importable import g
import inspect


def test_import_state_and_mem_loc():

    class_type = Group
    module_name = "importable"

    module = importlib.import_module(module_name)
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, class_type) and obj is not class_type:
            g_importlib = obj

    g._add_member("member_from_direct_import")
    g_importlib._add_member("member_from_importlib")

    logging.debug(f"Members: {g._members}")
    assert g_importlib._members == g._members

    assert g_importlib == g
    assert id(g_importlib) == id(g)
    assert g_importlib is g

    # but then with an higher order path
    sys.path.append(str(Path(__file__).parent.parent))

    abs_module = importlib.import_module("tests.importable")
    for _, obj in inspect.getmembers(abs_module):
        if isinstance(obj, class_type) and obj is not class_type:
            g_abs_import = obj

        logging.debug(f"Members: {g._members}")

    assert g_abs_import == g, "Pass the basic comparison"
    assert id(g_abs_import) != id(
        g
    ), "But actually you are at a different memory location"
    assert g_abs_import is not g, "And you are not the same object"
