import aiohttp
import asyncio
import os

import redis
from hail.models.configuration import ETMScenario
from hail.context import ContextProvider
from hail.models.request import MunicipalityScenario
from hail.models.response import APIResponse, ScenarioData
from hail.util import filter_dict
from hail.cache import rediscache
from tenacity import retry, wait_exponential, stop_after_delay, after_log
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

RETRY_KWARGS = dict(
    wait=wait_exponential(multiplier=1, min=0.2, max=1),
    stop=stop_after_delay(5),
    after=after_log(logger, logging.DEBUG),
)


class AsyncETMClient:

    def __init__(
        self,
        main_scenario: str,
        scenarios: list[ETMScenario],
        base_url: str = "https://engine.energytransitionmodel.com/",
        api_key: str = None,
        redis_client: redis.Redis = None,
    ) -> None:
        self.base_url = base_url
        self.main_scenario = main_scenario

        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("ETM_API_KEY")

        self.scenarios = scenarios

        if redis_client is not None:
            self._redis_client = redis_client

    @property
    def redis_client(self) -> redis.Redis:
        try:
            return self._redis_client
        except AttributeError:
            raise AttributeError(
                "No redis client has been set. Please set a redis client (.set_redis_client) before trying to access it."
            )

    @property
    def scenarios(self) -> list[ETMScenario]:
        return self._scenarios

    @scenarios.setter
    def scenarios(self, value: list[ETMScenario] | list):
        if value:
            self._scenarios = [
                ETMScenario(
                    name=scenario.name,
                    etm_id=scenario.etm_id,
                    selectedScenario=self.main_scenario,
                    user_values=scenario.user_values,
                )
                for scenario in value
            ]

    @rediscache
    @retry(**RETRY_KWARGS)
    async def _scenario_put_client(
        self,
        *,
        scenario: ETMScenario,
        session: aiohttp.ClientSession,
        body: dict,
        redis_client: redis.Redis,
    ) -> dict:
        """Do the put operation on a single scenario for a list of gqueries and return the response."""
        try:
            async with session.put(url=scenario.url_path, json=body) as response:
                resp = await response.json()

                if response.status != 200:
                    logger.error(
                        f"Failed to get put on {scenario.etm_id}: {response.reason}"
                    )
                    raise ConnectionError(
                        f"Unable to put on {scenario.etm_id} due to {e.__class__}"
                    )
                else:
                    logger.debug(
                        f"Successfully ({response.status}) put on {scenario.etm_id} for {len(body['gqueries'])} gqueries."
                    )
        except Exception as e:
            logger.error(
                "Unable to put on {} due to {}.".format(scenario.etm_id, e.__class__)
            )
            raise e
        return resp

    async def scenario_put(
        self,
        scenario: ETMScenario,
        session: aiohttp.ClientSession,
        gqueries: list[str],
    ) -> dict:
        """Do the put operation on a single scenario for a list of gqueries and return the response.
        We need this intermediate function to create the body of the request (which we use for the cache key).
        """

        body = {
            "gqueries": gqueries,  # ensure that the gqueries are a list
        }

        # ETM scenario
        logging.debug(f"User values [{scenario.etm_id}]: {scenario.user_values}")
        if scenario.user_values is not None:
            body.update(
                {
                    "user_values": scenario.user_values,
                }
            )

        return await self._scenario_put_client(
            scenario=scenario,
            session=session,
            body=body,
            redis_client=self.redis_client,
        )

    @rediscache
    @retry(**RETRY_KWARGS)
    async def get_inputs(
        self,
        *,
        scenario: ETMScenario,
        session: aiohttp.ClientSession,
        inputs: list[str],
        redis_client: redis.Redis,
    ) -> dict:
        """Query a single scenario for a list of inputs and return the response."""
        inputs_url = scenario.url_path + "/inputs"
        try:
            async with session.get(url=inputs_url) as response:
                resp = await response.json()

                if response.status != 200:
                    logger.error(
                        f"Failed to get inputs for{scenario.etm_id}: {response.reason}"
                    )
                    raise ConnectionError(
                        f"Unable to get inputs on {scenario.etm_id}: {response.reason}"
                    )
                else:
                    logger.debug(
                        f"Successfully ({response.status}) got inputs on {scenario.etm_id}"
                    )
        except Exception as e:
            logger.error(
                "Unable to get inputs for {} due to {}.".format(
                    scenario.etm_id, e.__class__
                )
            )
            raise e

        return filter_dict(resp, inputs)

    async def query(
        self,
        scenario: ETMScenario,
        session: aiohttp.ClientSession,
        gqueries: list[str] = None,
        inputs: list[str] = None,
    ) -> dict:
        """Query a single scenario for gqueries and inputs and return the response."""

        inputs_task = (
            self.get_inputs(
                scenario=scenario,
                session=session,
                inputs=inputs,
                redis_client=self.redis_client,
            )
            if inputs
            else None
        )
        scenario_task = self.scenario_put(scenario, session, gqueries)

        if inputs_task:
            scenario_response, inputs_response = await asyncio.gather(
                scenario_task, inputs_task
            )
            return {**scenario_response, "inputs": inputs_response}
        else:
            scenario_response = await scenario_task
            return {**scenario_response, "inputs": {}}

    async def query_all(
        self,
        gqueries: list[str] = None,
        inputs: list[str] = None,
    ) -> list[dict]:
        """Query all scenarios for a list of gqueries and return a list of responses."""

        headers = {}
        headers["Authorization"] = f"Bearer {self.api_key}"

        async with aiohttp.ClientSession(base_url=self.base_url) as session:
            ret = await asyncio.gather(
                *(
                    self.query(scenario, session, gqueries, inputs)
                    for scenario in self.scenarios
                )
            )

        return ret

    async def connect_raw(
        self, gqueries: set[str] = None, inputs: set[str] = None, ui: set[str] = None
    ) -> list[APIResponse]:
        """Return a list of APIResponse objects."""
        unvalidated_responses = await self.query_all(gqueries, inputs)
        validated_responses = [
            APIResponse(**response) for response in unvalidated_responses
        ]
        return validated_responses

    def _get_raw_response(self, gqueries: list[str]) -> list[dict]:
        """Return a list of raw response dictionaries (debug only)"""
        return asyncio.run(self.query_all(gqueries))

    async def connect(
        self,
        gqueries: set[str] = None,
        inputs: set[str] = None,
        ui: set[str] = None,
    ) -> ContextProvider:
        """Return a ContextProvider object for the rest of the response."""

        responses = await self.connect_raw(gqueries, inputs, ui)
        return ContextProvider.from_response(responses, accessed_attributes_ui=ui)

    @retry(**RETRY_KWARGS)
    async def copy_single_scenario(
        self, ms: MunicipalityScenario
    ) -> MunicipalityScenario:
        url = self.base_url + "api/v3/scenarios"
        headers = {
            "Accept": "application/json",
            # "Authorization": f"Bearer {self.api_key}",
            # ^^ bug, reported: https://github.com/quintel/etengine/issues/1460
        }
        scenario_id = ms.ETMscenarioID
        data = {"scenario": {"scenario_id": str(scenario_id)}}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                resp = await response.json()

                if response.status != 200:
                    logger.debug(
                        f"Failed to copy scenario {scenario_id}: {response.reason}. Body: {data}. Response: {resp}"
                    )
                    raise ConnectionError(
                        f"Failed to copy scenario {scenario_id}: {response.reason}"
                    )
                else:
                    logger.debug(
                        f"Successfully copied scenario {scenario_id} with new ID {resp.get('id')}"
                    )

                valid_resp = ScenarioData(**resp)

                return MunicipalityScenario(
                    municipalityID=ms.municipalityID,
                    ETMscenarioID=valid_resp.id,
                )

    async def copy_scenarios(
        self, base_scenarios: list[MunicipalityScenario]
    ) -> list[MunicipalityScenario]:
        """Copy existing scenarios by their IDs and return the response."""

        tasks = [self.copy_single_scenario(ms) for ms in base_scenarios]
        responses = await asyncio.gather(*tasks)

        return responses
