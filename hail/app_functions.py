import logging
from pathlib import Path

from redis import Redis
from hail.client import AsyncETMClient
from hail.context import ContextProvider
from hail.development import AbstractDevelopment
from hail.generate import (
    compute_all_etm_setters,
    compute_response_post_update,
    import_all_classes_from_folder,
)
from hail.models.calculate import CalculateResponse
from hail.models.configuration import AccessedAttributes, ETMScenario
from hail.models.enums import MainScenarioEnum
from hail.models.request import PostUserInputRequest
from hail.models.state import PreloadedState
from hail.result import AbstractResultMap
from hail.result.graph import AbstractResultGraph
from tests.mock_context import MockMultiScenarioDataWrapper
from config.aggregation import configs as aggregation_configs

# TODO: clean up in terms of naming convention, hail.models uses calculate, but the source is hail.generate and in there we call it compute...?
# this should only happen before we make changes on initial load or if we want the values at municipality level
# otherwise, we should aggregate based on the values of the updated scenario


def mock_context(
    request: PostUserInputRequest, accessed_attributes: AccessedAttributes
) -> ContextProvider:
    return ContextProvider(
        MockMultiScenarioDataWrapper(
            num_scenarios=len(request.userSettings.municipalityScenarios),
            actual_ids=[
                ms.ETMscenarioID for ms in request.userSettings.municipalityScenarios
            ],
        ),
        _ui_fields=accessed_attributes.ui,
    )


async def initial_context_call(
    request: PostUserInputRequest,
    accessed_attributes: AccessedAttributes,
    redis_client: Redis,
) -> ContextProvider:
    # create a list of scenarios to be used in the ETM client
    scenarios = [
        ETMScenario(
            name=ms.municipalityID,
            etm_id=ms.ETMscenarioID,
        )
        for ms in request.userSettings.municipalityScenarios
    ]

    # this should be done for each request as every request can have different scenarios
    client = AsyncETMClient(
        main_scenario=request.userSettings.selectedScenario,
        scenarios=scenarios,
        redis_client=redis_client,
    )

    # this block interacts with the ETM and sets the context for all calculations (in this tool)
    # ! We should get the state of the ETM scenarios to be able to correctly define the input values
    # TODO: make sure this logic is not flawed due to the state of the ETM scenarios (e.g. convergence)
    # TODO: In principle, we should always hit cache for non-updated scenario's if we solely base this on area codes
    # E.g., hash the input differently for scenarios without user_values (request.UserSettings.<con/sec>Developments is None)
    return await client.connect(
        gqueries=accessed_attributes.gqueries,
        inputs=accessed_attributes.inputs,
        ui=accessed_attributes.ui,
    )


async def make_response(context: ContextProvider):
    """Compute the response based on the context"""

    input, map, graph, msgs = await compute_response_post_update(context=context)

    # parse the input to the response object
    return CalculateResponse(input=input, map=map, graph=graph, msgs=msgs)


async def update_context(
    request: PostUserInputRequest,
    initial_context: ContextProvider,
    accessed_attributes: AccessedAttributes,
    redis_client: Redis,
) -> ContextProvider:

    # calculate the new etm scenarios based on the original scenario values (through context)
    updated_etm_scenarios = compute_all_etm_setters(
        context=initial_context,
    )

    # connect again on the ETM, this time with updated parameters (on which to base the results)
    # TODO: if this re-initiation takes time, maybe just update scenario's on the original client object
    updated_client = AsyncETMClient(
        main_scenario=request.userSettings.selectedScenario,
        scenarios=updated_etm_scenarios,
        redis_client=redis_client,
    )

    updated_context = await updated_client.connect(
        gqueries=accessed_attributes.gqueries,
        inputs=accessed_attributes.inputs,
        ui=accessed_attributes.ui,
    )
    updated_context.add_request(request=request)
    # TODO: Unsure if we need this at all, as we only use the original context to determine ETM-setters
    updated_context.add_original_context(initial_context)

    return updated_context


def get_palettes():
    import colorcet as cc

    palettes = [
        (name, getattr(cc, name)) for name in cc.__dir__() if name.startswith("b_")
    ]

    from hail.util import render_template

    template_fp = Path(__file__).parent / "hail" / "util" / "swatch.html.jinja"
    return render_template(template_fp, palettes=palettes)


def get_mapclasses(configpath: Path) -> list[AbstractResultMap]:

    classes: list[AbstractResultMap] = import_all_classes_from_folder(
        configpath, AbstractResultMap
    )
    return classes


def get_developmentclasses(configpath: Path) -> list[AbstractDevelopment]:
    classes: list[AbstractDevelopment] = import_all_classes_from_folder(
        configpath, AbstractDevelopment
    )
    return classes


def get_graphclasses(configpath: Path) -> list[AbstractResultGraph]:

    classes: list[AbstractResultGraph] = import_all_classes_from_folder(
        configpath, AbstractResultGraph
    )
    return classes


def get_aggregation_configs(configpath: Path) -> list[AbstractResultGraph]:

    for conf in aggregation_configs:
        conf.load(configpath=configpath)

    return aggregation_configs


async def get_main_graph(
    selected_scenario: MainScenarioEnum,
    preloaded: PreloadedState,
    redis_client: Redis,
) -> CalculateResponse:

    accessed_attributes = preloaded.accessed_attributes
    scenario_relations = preloaded.scenario_relations
    energy_balance_graph = [
        graph for graph in preloaded.graphclasses if graph.key == "energybalance_bar"
    ][0]

    for scenario_rel in scenario_relations:
        if scenario_rel.main_scenario == selected_scenario:
            base_scenarios = scenario_rel.municipal_scenarios

    default_scenarios = [
        ETMScenario(
            name=ms.municipalityID,
            etm_id=ms.ETMscenarioID,
        )
        for ms in base_scenarios
    ]

    client = AsyncETMClient(
        main_scenario=selected_scenario,
        scenarios=default_scenarios,
        redis_client=redis_client,
    )

    context = await client.connect(
        gqueries=accessed_attributes.gqueries,
        inputs=accessed_attributes.inputs,
        ui=accessed_attributes.ui,
    )

    graph = energy_balance_graph.make_graph_toplevel(context)

    return CalculateResponse(graph=graph)


def log_reason_postuservalues(request: PostUserInputRequest, changes_by_user: bool):
    if request.viewSettings.original is True:
        logging.info(
            "[app:post_user_values] Returning original results because viewSettings.original is True"
        )
    elif not changes_by_user:
        logging.info(
            "[app:post_user_values] Returning original results because no changes by user"
        )
    else:
        logging.info(
            "[app:post_user_values] Returning updated results because changes by user"
        )
