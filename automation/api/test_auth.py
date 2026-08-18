import os

import requests
from config import BASE_URL

QA_USERNAME = os.getenv("QA_USERNAME")
QA_PASSWORD = os.getenv("QA_PASSWORD")


def test_login_with_invalid_credentials():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "invalid_test_user_12345",
            "password": "wrong_password_12345"
        }
    )


    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong username or password"


def test_login_with_valid_credentials():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": QA_USERNAME,
            "password": QA_PASSWORD
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"