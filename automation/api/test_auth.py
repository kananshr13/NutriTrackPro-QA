import os

import pytest
import requests

from config import BASE_URL

QA_USERNAME = os.getenv("QA_USERNAME")
QA_PASSWORD = os.getenv("QA_PASSWORD")


@pytest.mark.negative
@pytest.mark.regression
def test_login_with_invalid_credentials():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "invalid_test_user_12345",
            "password": "wrong_password_12345"
        }
    )

    assert response.status_code == 401

    response_data = response.json()

    assert isinstance(response_data, dict)
    assert "detail" in response_data
    assert isinstance(response_data["detail"], str)
    assert response_data["detail"] == "Wrong username or password"


@pytest.mark.smoke
@pytest.mark.regression
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

    assert isinstance(response_data, dict)

    assert "access_token" in response_data
    assert isinstance(response_data["access_token"], str)
    assert len(response_data["access_token"]) > 0

    assert "token_type" in response_data
    assert isinstance(response_data["token_type"], str)
    assert response_data["token_type"] == "bearer"


@pytest.mark.negative
@pytest.mark.regression
def test_login_without_username():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "password": QA_PASSWORD
        }
    )

    assert response.status_code == 422


@pytest.mark.negative
@pytest.mark.regression
def test_login_without_password():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": QA_USERNAME
        }
    )

    assert response.status_code == 422


@pytest.mark.negative
@pytest.mark.regression
def test_login_with_empty_credentials():
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "",
            "password": ""
        }
    )

    assert response.status_code in [401, 422]