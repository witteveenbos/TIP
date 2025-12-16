#!/usr/bin/env python3
"""
Cache warming script for the hail application.
This script pre-populates Redis cache by calling key API endpoints after container startup.
"""
import asyncio
import httpx
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = os.getenv("HAIL_BASE_URL", "http://localhost:7000")
TIMEOUT = 300  # 5 minutes timeout for each request
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


async def wait_for_service(base_url: str, max_attempts: int = 30, delay: int = 2):
    """Wait for the service to be ready before warming cache."""
    logger.info(f"Waiting for service at {base_url} to be ready...")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for attempt in range(max_attempts):
            try:
                response = await client.get(f"{base_url}/list_scenarios/")
                if response.status_code == 200:
                    logger.info("Service is ready!")
                    return True
            except Exception as e:
                logger.debug(f"Attempt {attempt + 1}/{max_attempts}: Service not ready yet - {e}")
            
            await asyncio.sleep(delay)
    
    logger.error(f"Service failed to become ready after {max_attempts} attempts")
    return False


async def get_scenarios(base_url: str):
    """Fetch the list of available scenarios."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{base_url}/list_scenarios/")
            response.raise_for_status()
            scenarios = response.json()
            logger.info(f"Found {len(scenarios)} scenarios to warm cache for")
            return scenarios
        except Exception as e:
            logger.error(f"Failed to fetch scenarios: {e}")
            return []


async def warm_main_graph(base_url: str, scenario_data_link: str):
    """Warm cache for main graph endpoint."""
    url = f"{base_url}/get_main_graph/"
    params = {"main_scenario": scenario_data_link}
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Warming main graph cache for scenario: {scenario_data_link}")
                response = await client.get(url, params=params)
                response.raise_for_status()
                logger.info(f"✓ Successfully warmed main graph cache for {scenario_data_link}")
                return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {scenario_data_link}: {e}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
    
    logger.error(f"✗ Failed to warm main graph cache for {scenario_data_link} after {MAX_RETRIES} attempts")
    return False


async def warm_cache_for_scenario(base_url: str, scenario: dict, config_path: Path) -> bool:
    """Warm cache for a single scenario."""
    data_link = scenario.get("dataLink")
    title = scenario.get("title", data_link)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing scenario: {title}")
    logger.info(f"{'='*60}")
    
    # Warm main graph cache
    return await warm_main_graph(base_url, data_link)


async def main():
    """Main cache warming routine."""
    logger.info("=" * 80)
    logger.info("Starting Redis cache warming for hail application")
    logger.info("=" * 80)
    
    # Wait for the service to be ready
    if not await wait_for_service(BASE_URL):
        logger.error("Service did not become ready in time. Exiting.")
        sys.exit(1)
    
    # Determine config path
    config_path = Path(__file__).parent.parent / "config"
    if not config_path.exists():
        logger.error(f"Config path not found: {config_path}")
        sys.exit(1)
    
    # Get list of scenarios
    scenarios = await get_scenarios(BASE_URL)
    if not scenarios:
        logger.error("No scenarios found. Cache warming aborted.")
        sys.exit(1)
    
    # Warm cache for each scenario
    successful = 0
    failed = 0
    
    for scenario in scenarios:
        try:
            result = await warm_cache_for_scenario(BASE_URL, scenario, config_path)
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            logger.error(f"Error processing scenario {scenario.get('title', 'unknown')}: {e}")
            failed += 1
    
    logger.info("\n" + "=" * 80)
    logger.info(f"Cache warming completed!")
    logger.info(f"Successful: {successful} scenarios")
    logger.info(f"Failed: {failed} scenarios")
    logger.info("=" * 80)
    
    if failed > 0:
        logger.warning("Some scenarios failed to warm cache. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Cache warming interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error during cache warming: {e}")
        sys.exit(1)
