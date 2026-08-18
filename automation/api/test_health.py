import pytest
import requests

from config import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
def test_api_is_reachable():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200