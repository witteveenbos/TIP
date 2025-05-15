# tests/fixtures/example_scenarios.json
import json
import pytest
from fastapi.testclient import TestClient
from app import app
from hail.models.request import PostUserInputRequest, MunicipalityScenario
from hail.models.calculate import CalculateResponse
from hail.models.enums import DevelomentType, AreaDivisionEnum

from pathlib import Path

# Load the fixture data


client = TestClient(app)


@pytest.mark.skip(reason="no way of currently testing this")
def test_post_user_values(request_without_changes: PostUserInputRequest):
    response = client.post(
        "/post_user_values", json=request_without_changes.model_dump(mode="json")
    )
    assert response.status_code == 200, response.json()
    data = response.json()
    assert "input" in data
    assert isinstance(data, CalculateResponse), response.json()
