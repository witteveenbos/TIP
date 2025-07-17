import hashlib
import json
import os
import redis.asyncio as redis
import logging
from contextlib import asynccontextmanager
from hail.models.configuration import ETMScenario

logger = logging.getLogger(__name__)


async def get_redis_client():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_password = os.getenv("REDIS_PASSWORD", None)
    print(f"Connecting to Redis at {redis_host}:{redis_port}")
    r = redis.Redis(host=redis_host, port=redis_port, db=0, ssl=False)
    try:
        yield r
    finally:
        await r.close()


async def generate_cache_key(body: str, scenario: ETMScenario) -> str:

    # generate a hash of the body
    key = hashlib.md5(body.encode("utf-8")).hexdigest()

    if scenario.user_values is None:
        # if no user values are provided, we can recycle the base scenario through the area code (name) and main scenario
        # i.e. all basic scenario's are based on the same cache key
        key = f"query::{scenario.selectedScenario.name}/{scenario.name}/{key}"
    else:
        # if user values are provided, we base the cache key on
        # scenario itself and the hash of the body
        key = f"query::{scenario.name}/{scenario.etm_id}/{key}"

    return key


async def _get_from_cache(
    redis_client: redis.Redis, cache_key: str, scenario: ETMScenario
) -> dict:
    # async with redis_client as r:
    r = redis_client
    try:
        data = await r.get(cache_key)
        if data is not None:
            logger.debug(f"Cache hit for {cache_key}")
            data = json.loads(data.decode("utf-8"))

            # if we hit a generic cache, make sure act as if this is the response of this specific scenario
            if scenario.selectedScenario.name in cache_key and "query" in cache_key:
                data["scenario"]["id"] = scenario.etm_id

        else:
            logger.debug(f"Cache miss for {cache_key}")
        return data
    except Exception as e:
        logger.error(f"Error accessing Redis for cache key {cache_key}: {str(e)}")
        logger.error(f"Redis connection: Host {r.connection_pool.connection_kwargs['host']}, Port {r.connection_pool.connection_kwargs['port']}")
        return None


async def _set_cache(redis_client: redis.Redis, cache_key: str, data: dict) -> None:
    # async with redis_client as r:
    r = redis_client
    try:
        await r.set(cache_key, json.dumps(data))
    except Exception as e:
        logger.error(f"Error setting Redis cache for key {cache_key}: {str(e)}")
        logger.error(f"Redis connection: Host {r.connection_pool.connection_kwargs['host']}, Port {r.connection_pool.connection_kwargs['port']}")


def rediscache(func):
    async def wrapper(self, *args, **kwargs):

        no_cache = bool(int(os.getenv("NO_CACHE", False)))

        # Disable cache if NO_CACHE environment variable is set to True
        if no_cache:
            return await func(self, *args, **kwargs)

        if "body" in kwargs:
            body: dict = kwargs["body"]
            scenario: ETMScenario = kwargs["scenario"]
            # sort body to ensure consistent cache key
            body = json.dumps(body, sort_keys=True)
            cache_key = await generate_cache_key(body, scenario)

        elif "inputs" in kwargs and "scenario" in kwargs:
            scenario: ETMScenario = kwargs["scenario"]
            cache_key = f"inputs::{scenario.selectedScenario.name}/{scenario.name}"

        redis_client = kwargs.get("redis_client", get_redis_client())

        response = await _get_from_cache(
            redis_client=redis_client, cache_key=cache_key, scenario=scenario
        )

        if response is not None:
            return response

        response = await func(self, *args, **kwargs)

        await _set_cache(redis_client=redis_client, cache_key=cache_key, data=response)

        return response

    return wrapper
