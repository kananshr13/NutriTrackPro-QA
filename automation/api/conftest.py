import os

import pytest
import requests
from config import BASE_URL


@pytest.fixture
def auth_token():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": os.getenv("QA_USERNAME"),
            "password": os.getenv("QA_PASSWORD")
        }
    )


    assert response.status_code == 200

    return response.json()["access_token"]