import requests

from config import BASE_URL


def test_api_is_reachable():
    response = requests.get(BASE_URL)

    assert response.status_code != 500