import inspect
import re

from hail.generate import import_all_classes_from_folder
from hail.models.request import (
    PostUserInputRequest,
)
from hail.models.response import QueryResult, InputResult
from hail.models.matrix import Matrix
from hail.context import ContextProvider
from hail.development import AbstractDevelopment
from pathlib import Path
import logging
from hail.generate import compute_all_developments

from hail.models.state import PreloadedState
from tests.mock_context import MockMultiScenarioDataWrapper, mock_context_provider

import config.developments.shared as shared_module

CONFIG = Path(__file__).parent.parent / "config"


def test_fields_against_incorrect_implementation():
    classes = import_all_classes_from_folder(
        Path(__file__).parent.parent / "config", AbstractDevelopment
    )
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")

    forbidden_pattern_initiation = r".TOTAL"
    forbidden_pattern_initiation_and_setters = r"sum\(.*\)|sum\(\n.*\n\)"
    # inspect methods [min, max and default] for pressence
    # --> and .TOTAL (which is a property of Group)
    # ^^ we could make that more specific, but it's not necessary
    # these are not allowed due to introduction of a cyclic dependency

    # add all functions from shared to the list

    all_members = inspect.getmembers(shared_module)
    functions = [member[1] for member in all_members if inspect.isfunction(member[1])]

    classes += functions

    for cls in classes:
        for method_name in ["min", "max", "default", "sets_ETM_value"]:
            if inspect.isclass(cls):
                try:
                    _ = cls()
                    method = getattr(cls, method_name, None)
                    # method must exist due to AbstractDevelopment
                    source = inspect.getsource(method)
                except TypeError:
                    logging.info(
                        f"Could not instantiate {cls.__name__}. Check for abstract methods."
                    )
            else:
                # TODO: cls is actually a function (dirty)
                source = inspect.getsource(cls)

            if method_name == "sets_ETM_value" or not inspect.isclass(cls):
                # ^^ this assumes that all shared functions are only used for the sets_ETM_value method
                forbidden_patterns = [forbidden_pattern_initiation_and_setters]
            else:
                forbidden_patterns = [
                    forbidden_pattern_initiation,
                    forbidden_pattern_initiation_and_setters,
                ]
            for pattern in forbidden_patterns:
                logging.debug(f"Checking {cls.__name__}.{method_name} for {pattern}")
                matches = re.search(pattern, source)
                assert (
                    not matches
                ), f"Found forbidden pattern (gquery.future or inputs.user) in {cls.__name__}.{method_name}: {matches.string}"


def test_all_classes_against_wrong_total_implementation():
    config_path = Path(__file__).parent.parent / "config"
    pattern = r"^(?!var\.).*\.TOTAL$"

    py_files = config_path.rglob("*.py")
    for py_file in py_files:
        with open(py_file, "r") as file:
            content = file.read()
            matches = re.match(pattern, content)
            assert (
                not matches
            ), f"Found out-dated implemenation of .TOTAL in {py_file}: {matches}, use var.groups.<group>.TOTAL instead."


def test_etm_setters_static():
    classes: list[AbstractDevelopment] = import_all_classes_from_folder(
        CONFIG, AbstractDevelopment
    )
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")

    mock_context_provider.set_groups(classes)
    for group in mock_context_provider.groups.values():

        logging.debug(f"Checking group {group.name}")
        logging.debug(f"Members: {group._members}")
        logging.debug(f"Group total: {group.TOTAL}")

    for cls in classes:
        # get the return value of the method
        try:
            value = cls.sets_ETM_value(mock_context_provider)
            # assert type of value is dict
            if value is None:
                logging.info("Method sets_ETM_value returned None. Skipping test.")
            assert isinstance(
                value, dict
            ), f"Expected dict, got {type(value)} from {cls.__name__}.sets_ETM_value"
            for lhs, rhs in value.items():
                assert (
                    isinstance(lhs, (QueryResult, InputResult))
                    or lhs.is_input_result  # due to the simplification of the MockMultiScenarioDataWrapper
                ), f"Expected QueryResult or InputResult, got {type(lhs)} from {cls.__name__}.sets_ETM_value"
                assert isinstance(
                    rhs, Matrix
                ), f"Expected Matrix got {type(rhs)} from {cls.__name__}.sets_ETM_value on {lhs.name}"
        except (NotImplementedError, TypeError) as e:
            logging.info(
                f"Method sets_ETM_value not implemented for {cls.__name__}. Skipping test."
            )
            if isinstance(e, TypeError):
                raise TypeError(
                    "Wrong implementation of Matrix manipulation for this object. Make sure you work on the right attribute (.min, .max or .default for inputs and .future or .present for gqueries)."
                )


def test_development_min_max_default():
    classes = import_all_classes_from_folder(CONFIG, AbstractDevelopment)
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")

    mock_context_provider.set_groups(classes)
    for group in mock_context_provider.groups.values():

        logging.debug(f"Checking group {group.name}")
        logging.debug(f"Members: {group._members}")
        logging.debug(f"Group total: {group.TOTAL}")

    for cls in classes:
        for method in ["min", "max", "default"]:
            # get the return value of the method
            try:
                value = getattr(cls(), method)(mock_context_provider)
                # assert type of value is dict
                if value is None:
                    logging.info(f"Method {method} returned None. Skipping test.")
                assert isinstance(value, Matrix), f"Expected Matrix, got {type(value)}"
            except (NotImplementedError, TypeError) as e:
                logging.info(
                    f"Method sets_ETM_value not implemented for {cls.__name__}. Skipping test."
                )
                if isinstance(e, TypeError):
                    raise TypeError(
                        "Wrong implementation of Matrix manipulation for this object. Make sure you work on the right attribute (.min, .max or .default for inputs and .future or .present for gqueries)."
                    )


def test_compute_development_min_max_default_logic(
    request_without_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    mock_context = ContextProvider(
        MockMultiScenarioDataWrapper.from_actual_ids(
            [
                subscen.ETMscenarioID
                for subscen in request_without_changes.userSettings.municipalityScenarios
            ]
        ),
        _ui_fields=preloaded_state.accessed_attributes.ui,
    )
    mock_context.add_request(request_without_changes)
    mock_context.add_preloaded(preloaded_state)
    compute_all_developments(
        method="make_developments",
        context=mock_context,
    )
