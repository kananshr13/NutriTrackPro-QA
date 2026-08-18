import os

import pytest
import requests
from dotenv import load_dotenv

from config import BASE_URL

load_dotenv()


@pytest.fixture(scope="session")
def auth_token():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": os.getenv("QA_USERNAME"),
            "password": os.getenv("QA_PASSWORD")
        }
    )

    assert response.status_code == 200, (
        f"Login failed: {response.status_code} - {response.text}"
    )

    return response.json()["access_token"]