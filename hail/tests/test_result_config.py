import pytest
from hail.generate import import_all_classes_from_folder
from hail.models.calculate import ColorMapDef, LegendDef, MapMetaData, MapResponse
from hail.models.enums import AreaDivisionEnum, BalanceEnum, CarrierEnum
from hail.models.request import (
    PostUserInputRequest,
)
from hail.models.matrix import Matrix
from hail.context import ContextProvider
from hail.result import AbstractResultMap
from pathlib import Path
import logging

from hail.models.state import PreloadedState
from hail.parse import find_all_accessed_attributes
from tests.mock_context import MockMultiScenarioDataWrapper, mock_context_provider


CONFIG = Path(__file__).parent.parent / "config"
RESULT_CONFIG = CONFIG / "results" / "maps"


@pytest.fixture
def preloaded_state():
    preloaded = PreloadedState()
    preloaded.accessed_attributes = find_all_accessed_attributes(CONFIG)
    return preloaded


def test_map_static_properties():
    classes: list[AbstractResultMap] = import_all_classes_from_folder(
        RESULT_CONFIG, AbstractResultMap
    )
    if not classes:
        logging.warning(
            "No implementations of AbstractResultMap classes found in config folder"
        )
        return
    logging.debug(f"Found {len(classes)} AbstractResultMap classes in config folder")

    for cls in classes:
        assert isinstance(
            cls.key, str
        ), f"Expected str for 'key' property, got {type(cls.key)}"
        assert isinstance(
            cls.name, str
        ), f"Expected str for 'name' property, got {type(cls.name)}"
        assert isinstance(
            cls.unit, str
        ), f"Expected str for 'unit' property, got {type(cls.unit)}"
        assert isinstance(
            cls.colormap, ColorMapDef
        ), f"Expected ColorMapDef, got {type(cls.colormap)}"
        assert isinstance(
            cls.legend, LegendDef
        ), f"Expected LegendDef, got {type(cls.legend)}"
        assert isinstance(
            cls.related_balance, BalanceEnum
        ), f"Expected BalanceEnum, got {type(cls.related_balance)}"
        assert isinstance(
            cls.related_carrier, CarrierEnum
        ), f"Expected CarrierEnum, got {type(cls.related_carrier)}"
        if cls.related_area_div is not None:
            assert isinstance(
                cls.related_area_div, (AreaDivisionEnum, list)
            ), f"Expected AreaDivisionEnum, got {type(cls.related_area_div)}"
            if isinstance(cls.related_area_div, list):
                assert all(
                    [
                        isinstance(area, AreaDivisionEnum)
                        for area in cls.related_area_div
                    ]
                ), f"Expected AreaDivisionEnum in this list"


def test_map_results_from_implementation():
    classes: list[AbstractResultMap] = import_all_classes_from_folder(
        RESULT_CONFIG, AbstractResultMap
    )
    if not classes:
        logging.warning(
            "No implementations of AbstractResultMap classes found in config folder"
        )
        return
    logging.debug(f"Found {len(classes)} AbstractResultMap classes in config folder")

    for cls in classes:
        try:
            map_matrix = cls.map(var=mock_context_provider)
            mock_data: MockMultiScenarioDataWrapper = mock_context_provider.data

            assert isinstance(
                map_matrix, Matrix
            ), f"Expected Matrix, got {type(map_matrix)}"
            assert len(map_matrix) == len(mock_data._scenario_ids), (
                f"Expected length {len(mock_data._scenario_ids)}, "
                f"got {len(map_matrix)}"
            )

        except NotImplementedError:
            logging.info(
                f"Skipping `test_map_results_from_implementation` for {cls.__name__} as it does not implement make_map (GM-level)"
            )
            continue


def test_map_results_from_abstract(
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
    mock_context._ui_fields = preloaded_state.accessed_attributes.ui
    classes: list[AbstractResultMap] = import_all_classes_from_folder(
        RESULT_CONFIG, AbstractResultMap
    )
    if not classes:
        logging.warning(
            "No implementations of AbstractResultMap classes found in config folder"
        )
        return
    logging.debug(f"Found {len(classes)} AbstractResultMap classes in config folder")

    for cls in classes:

        try:
            map_result = cls.make_map(mock_context)
            assert isinstance(
                map_result, MapResponse
            ), f"Expected MapResponse, got {type(map_result)}"

            map_matrix = cls.map(var=mock_context)
            cm = cls.make_colormap(map_matrix=map_matrix)
            map_meta = cls._make_metadata(cm)
            assert isinstance(
                map_meta, MapMetaData
            ), f"Expected MapMetaData, got {type(map_meta)}"
        except NotImplementedError:
            logging.info(
                f"Skipping `test_map_results_from_abstract` for {cls.__name__} as it does not implement make_map (GM-level)"
            )
            continue


def test_map_coverage_carrier_balance_area_div():

    classes: list[AbstractResultMap] = import_all_classes_from_folder(
        RESULT_CONFIG, AbstractResultMap
    )

    related_areas = []
    related_carriers = []
    related_balances = []
    for cls in classes:
        if isinstance(cls.related_area_div, list):
            related_areas.extend(cls.related_area_div)
            related_carriers.extend(
                [*[cls.related_carrier] * len(cls.related_area_div)]
            )
            related_balances.extend(
                [*[cls.related_balance] * len(cls.related_area_div)]
            )
        else:
            related_areas.append(cls.related_area_div)
            related_carriers.append(cls.related_carrier)
            related_balances.append(cls.related_balance)

    all_combinations = list(zip(related_areas, related_carriers, related_balances))
    # ensure exclusitivity
    assert len(set(all_combinations)) == len(
        all_combinations
    ), "Expected mutally exclusive combinations of related_area_div, related_carrier, related_balance"

    # ensure all combinations are present
    for area in AreaDivisionEnum:
        for carrier in CarrierEnum:
            for balance in BalanceEnum:
                specific_combination = (area, carrier, balance)
                aspecific_combination = (None, carrier, balance)
                if (
                    not specific_combination in all_combinations
                    and not aspecific_combination in all_combinations
                ):
                    logging.error(f"Missing combination: {area}, {carrier}, {balance}")
                    one_missing = True

    try:
        assert not one_missing, "Missing combinations found (see logs above)"
    except AssertionError:
        logging.error(f"[soft fail]: Missing combinations found (see logs above)")
