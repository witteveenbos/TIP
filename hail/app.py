from contextlib import asynccontextmanager
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from fastapi.responses import HTMLResponse, FileResponse
from redis import Redis

from hail.log_middleware import LogMiddleware, get_logs, download_logs
from hail.models.configuration import DistributedScenarioRelation
from hail.models.calculate import CalculateResponse
from hail.client import AsyncETMClient
from hail.cache import get_redis_client
from hail.models.enums import MainScenarioEnum
from hail.models.state import PreloadedState
from hail.parse import find_all_accessed_attributes
from hail.models.request import (
    CreateScenariosRequest,
    MunicipalityScenario,
    PostUserInputRequest,
)
from hail.models.scenario import ScenarioDisplay
import app_functions as af
from hail.reference.graphs import GraphTypes

CONFIG = Path(__file__).parent / "config"
DEV_CONFIG = CONFIG / "developments"
RESULT_CONFIG = CONFIG / "results"
# TODO: use these config paths (optimization)

ORIGINS = [
    "http://localhost:3000",
    "https://pzh-pmiek-tooling-accept.azurewebsites.net",
    "https://pzh-pmiek-tooling.azurewebsites.net",
]


# this is done during the startup (when the server starts)
# because we are using the same config for all requests
preloaded = PreloadedState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # find all the accessed attributes in the config for UI developments
    preloaded.accessed_attributes = find_all_accessed_attributes(CONFIG)

    # get configuration for scenarios and aggregation
    preloaded.scenario_display = ScenarioDisplay.multiple_from_config(CONFIG)
    preloaded.scenario_relations = DistributedScenarioRelation.multiple_from_config(
        CONFIG
    )
    preloaded.aggregation_configs = af.get_aggregation_configs(CONFIG)

    ## find all classes and store them
    preloaded.mapclasses = af.get_mapclasses(RESULT_CONFIG)
    preloaded.graphclasses = af.get_graphclasses(RESULT_CONFIG)
    preloaded.developmentclasses = af.get_developmentclasses(CONFIG)

    # lock the state to prevent any changes since we share this variable across all requests
    preloaded.make_immutable()
    # TODO: should we add all classes to the preloaded state? We are now importing multiple times on every request
    yield
    # end of lifespan actions below
    # you can place post shutdown actions here


app = FastAPI(
    lifespan=lifespan,
    redirect_slashes=True,  # Has to be false otherwise '307 Temporary redirect'
)

# Add logging middleware
app.add_middleware(LogMiddleware)

# Allow CORS for specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logs endpoints
app.get("/logs", response_class=HTMLResponse)(get_logs)
app.get("/logs_download", response_class=FileResponse)(download_logs)


@app.get("/list_scenarios/")
async def get_scenario_list() -> list[ScenarioDisplay]:
    """Get the list of all scenarios"""
    return preloaded.scenario_display


@app.get("/get_main_graph/")
async def get_main_graph(
    main_scenario: MainScenarioEnum,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
) -> CalculateResponse:
    """Get the main graph (energy balance at second step of the scenario-select modal)"""
    async with redis_client as redis_client:
        return await af.get_main_graph(
            selected_scenario=main_scenario,
            preloaded=preloaded,
            redis_client=redis_client,
        )


@app.post("/create_municipality_scenarios/")
async def create_municipality_scenarios(
    request: CreateScenariosRequest,
) -> list[MunicipalityScenario]:
    """Create municipality scenarios"""

    client = AsyncETMClient(
        main_scenario=request.dataLink,
        scenarios=[],
    )

    for scenario_rel in preloaded.scenario_relations:
        if scenario_rel.main_scenario == request.dataLink:
            base_scenarios = scenario_rel.municipal_scenarios
            return await client.copy_scenarios(base_scenarios=base_scenarios)


@app.post("/post_user_values/")
async def post_user_values(
    request: PostUserInputRequest,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    mock_response: bool = False,
) -> CalculateResponse:
    """Post the current user values to determine the new results"""
    async with redis_client as redis_client:
        # point to the global preloaded state
        accessed_attributes = preloaded.accessed_attributes

        if mock_response:
            context = af.mock_context(request, accessed_attributes)
        else:
            context = await af.initial_context_call(
                request=request,
                accessed_attributes=accessed_attributes,
                redis_client=redis_client,
            )

        context.add_request(request)
        context.add_preloaded(preloaded)

        changes_by_user = (
            request.userSettings.continuousDevelopments
            or request.userSettings.sectoralDevelopments
        )
        if (
            not changes_by_user
            or request.viewSettings.original is True
            # or if the user wants to see the original results
        ):
            af.log_reason_postuservalues(
                request=request, changes_by_user=changes_by_user
            )
            context.disable_ui_propagation()
            return await af.make_response(
                context=context,
            )

        updated_context = await af.update_context(
            request=request,
            initial_context=context,
            accessed_attributes=accessed_attributes,
            redis_client=redis_client,
        )
        updated_context.add_preloaded(preloaded)

        af.log_reason_postuservalues(request=request, changes_by_user=changes_by_user)
        return await af.make_response(
            context=updated_context,
        )


@app.post("/flush_cache/")
async def flush_cache(super_secret_key: str) -> dict:

    if super_secret_key != os.getenv("SUPER_SECRET_KEY"):
        return {"message": "Invalid key, try again! ❌"}
    from hail.cache import get_redis_client

    async with get_redis_client() as redis:
        await redis.flushall()
    return {"message": "Cache flushed, cheers! 🍻"}


@app.get("/browse_palettes/", response_class=HTMLResponse)
def palettes():
    return af.get_palettes()


@app.get("/list_graphs/")
async def list_graphs() -> list[str]:
    graph_values = [graph.value for graph in GraphTypes]
    return graph_values
