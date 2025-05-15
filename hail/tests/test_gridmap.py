import logging
from pathlib import Path

from hail.context import ContextProvider
from hail.models.request import PostUserInputRequest
from hail.models.state import PreloadedState
from tests.mock_context import MockMultiScenarioDataWrapper
from config.results.maps._shared import get_dynamic_map_share


def test_dynamic_map_share(
    request_with_changes: PostUserInputRequest, preloaded_state: PreloadedState
):

    context = ContextProvider(
        MockMultiScenarioDataWrapper(
            num_scenarios=len(request_with_changes.userSettings.municipalityScenarios),
            actual_ids=[
                ms.ETMscenarioID
                for ms in request_with_changes.userSettings.municipalityScenarios
            ],
        ),
        _ui_fields=preloaded_state.accessed_attributes.ui,
    )

    context.add_preloaded(preloaded_state)
    context.add_request(request_with_changes)

    dynamic_map_share = get_dynamic_map_share(context)
