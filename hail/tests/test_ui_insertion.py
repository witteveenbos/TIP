import logging
from pathlib import Path

from hail.context import ContextProvider
from hail.development import AbstractDevelopment
from hail.generate import compute_all_etm_setters, import_all_classes_from_folder
from hail.models.calculate import ETMSetter
from hail.models.configuration import ETMScenario
from hail.models.fundamental import AttrDict
from hail.models.matrix import Matrix
from hail.models.request import PostUserInputRequest
from hail.models.response import InputResult, QueryResult
from hail.models.state import PreloadedState
from hail.util import id_to_region_map, region_to_id_map
from tests.mock_context import MockMultiScenarioDataWrapper, mock_context_provider


CONFIG = Path(__file__).parent.parent / "config"


def test_mappings_region_id_and_inverse(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui

    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    expected_id = 1
    expected_region = "GM0518"

    # Region to ID
    region_to_id = region_to_id_map(request_with_changes)
    assert isinstance(
        region_to_id, dict
    ), f"Expected dict, got {type(region_to_id)} from region_to_id_map"
    assert all(
        isinstance(key, str) for key in region_to_id.keys()
    ), "Expected str keys in region_to_id_map"
    assert all(
        isinstance(value, int) for value in region_to_id.values()
    ), "Expected int values in region_to_id_map"
    assert (
        expected_region in region_to_id
    ), f"Expected key '{expected_region}' not found in region_to_id_map."
    assert (
        region_to_id[expected_region] == expected_id
    ), f"Expected value '{expected_id}' for key '{expected_region}' in region_to_id_map, but found '{region_to_id[expected_region]}'."

    # ID to region
    id_to_region = id_to_region_map(request_with_changes)
    assert isinstance(
        id_to_region, dict
    ), f"Expected dict, got {type(id_to_region)} from id_to_region_map"
    assert all(
        isinstance(key, int) for key in id_to_region.keys()
    ), "Expected int keys in id_to_region_map"
    assert all(
        isinstance(value, str) for value in id_to_region.values()
    ), "Expected str values in id_to_region_map"
    assert (
        expected_id in id_to_region
    ), f"Expected key '{expected_id}' not found in id_to_region_map."
    assert (
        id_to_region[expected_id] == expected_region
    ), f"Expected value '{expected_region}' for key '{expected_id}' in id_to_region_map, but found '{id_to_region[expected_id]}'."


def test_insert_mock_request_sectoral(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui

    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    # Verify that the request is inserted at the correct key and position
    expected_key = "all_electric"
    expected_value = 33.3
    expexted_pos = 2

    # Ensure that the input is parsed to the expected format
    assert isinstance(
        mock_context_provider.ui, AttrDict
    ), "UI data object is not an instance of AttrDict"

    assert isinstance(
        mock_context_provider.ui[expected_key], Matrix
    ), "UI data object is not an instance of Matrix"

    # Ensure the key exists in the mock_context_provider.ui
    assert (
        expected_key in mock_context_provider.ui
    ), f"Expected key '{expected_key}' not found in mock_context_provider.ui."

    # Ensure the value is at the correct position in the matrix corresponding to the key
    matrix = mock_context_provider.ui[expected_key]
    assert (matrix[0:expexted_pos]) == [
        None,
        None,
    ], f"Expected None values at position 0 and 1 in the matrix, but found '{matrix[0:expexted_pos]}'"
    assert (
        matrix[expexted_pos] == expected_value
    ), f"Expected value '{expected_value}' at position 1 in the matrix, but found '{matrix[expexted_pos]}'."
    assert all(
        value is None for value in matrix[expexted_pos + 1 :]
    ), "Found unexpected non-None values in the matrix."


def test_insert_mock_request_continuous(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui

    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    # Verify that the request is inserted at the correct key and position
    expected_key = "zon_op_dak_huishoudens"
    expected_value = 10.0

    # Ensure that the input is parsed to the expected format
    assert isinstance(
        mock_context_provider.ui, AttrDict
    ), "UI data object is not an instance of AttrDict"

    assert isinstance(
        mock_context_provider.ui[expected_key], Matrix
    ), "UI data object is not an instance of Matrix"

    # Ensure the key exists in the mock_context_provider.ui
    assert (
        expected_key in mock_context_provider.ui
    ), f"Expected key '{expected_key}' not found in mock_context_provider.ui."

    # Ensure the value is at the correct position in the matrix corresponding to the key
    matrix = mock_context_provider.ui[expected_key]
    assert matrix[0] is None
    assert (
        matrix[1] == expected_value
    ), f"Expected value '{expected_value}' at position 1 in the matrix, but found '{matrix[1]}'."
    assert all(
        value is None for value in matrix[2:]
    ), "Found unexpected non-None values in the matrix."


def test_etm_setters_with_ui_insertion(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider = ContextProvider(
        MockMultiScenarioDataWrapper(
            num_scenarios=2,
            actual_ids=[1, 2],
        )
    )
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui

    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    classes = import_all_classes_from_folder(CONFIG, AbstractDevelopment)
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")

    mock_context_provider.set_groups(classes)

    for cls in classes:
        try:
            value = cls.sets_ETM_value(mock_context_provider)
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

                # We can't have a wider matrix than the number of scenarios
                assert len(rhs) == 2, f"Expected Matrix of length 2, got {len(rhs)}"

        except (NotImplementedError, TypeError) as e:
            logging.info(
                f"Method sets_ETM_value not implemented for {cls.__name__}. Skipping test."
            )
            if isinstance(e, TypeError):
                raise TypeError(
                    "Wrong implementation of Matrix manipulation for this object. Make sure you work on the right attribute (.min, .max or .default for inputs and .future or .present for gqueries)."
                )


def test_etm_setter_from_abstract(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui

    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    classes = import_all_classes_from_folder(CONFIG, AbstractDevelopment)
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")

    mock_context_provider.set_groups(classes)

    for cls in classes:
        cls: AbstractDevelopment = cls
        try:
            res = cls.determine_etm_setters(mock_context_provider)
        except NotImplementedError:
            logging.info(
                f"Method determine_etm_setters not implemented for {cls.__name__}. Skipping test."
            )
            continue
        assert isinstance(res, list), f"Expected list, got {type(res)}"

        for etm_setter_input_row in res:
            assert isinstance(
                etm_setter_input_row, list
            ), f"Expected list, got {type(etm_setter_input_row)}"
            for single_scenario_input_col in etm_setter_input_row:

                assert single_scenario_input_col is None or isinstance(
                    single_scenario_input_col, ETMSetter
                ), f"Expected None or ETMSetter, got {type(single_scenario_input_col)}"


def test_etm_setters_from_toplevel_compute(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    mock_context_provider = ContextProvider(
        MockMultiScenarioDataWrapper(
            2,
            actual_ids=[1, 2],
        )
    )

    # Set the preloaded UI fields in the mock context provider
    mock_context_provider._ui_fields = preloaded_state.accessed_attributes.ui
    # Insert the mock request
    mock_context_provider.add_request(request_with_changes)

    classes = import_all_classes_from_folder(CONFIG, AbstractDevelopment)
    if not classes:
        logging.warning("No classes found in config folder")
        return
    logging.info(f"Found {len(classes)} classes in config folder")
    preloaded_state.developmentclasses = classes

    mock_context_provider.set_groups(classes)
    mock_context_provider.add_preloaded(preloaded_state)

    updated_scenarios = compute_all_etm_setters(mock_context_provider)

    assert isinstance(
        updated_scenarios, list
    ), f"Expected list, got {type(updated_scenarios)}"
    for scenario in updated_scenarios:
        assert isinstance(
            scenario, ETMScenario
        ), f"Expected ETMScenario, got {type(scenario)}"

        if scenario.etm_id == 1:

            assert scenario.name == "GM0518", f"Expected 'GM0518', got {scenario.name}"

            assert scenario.user_values is not None, "Expected non-None user_values"

            assert (
                10.0 in scenario.user_values.values()
            ), "Expected value 10 in user_values"
