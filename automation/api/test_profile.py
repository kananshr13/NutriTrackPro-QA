import pytest
import requests

from config import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
def test_get_profile(auth_token):
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    profile_data = response.json()

    assert isinstance(profile_data, dict)

    if profile_data.get("profile") is not None:
        assert isinstance(profile_data["profile"], dict)


@pytest.mark.negative
@pytest.mark.regression
def test_get_profile_without_authentication():
    response = requests.get(
        f"{BASE_URL}/profile"
    )

    assert response.status_code in [401, 403]


@pytest.mark.negative
@pytest.mark.regression
def test_get_profile_with_invalid_token():
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": "Bearer invalid_token_12345"
        }
    )

    assert response.status_code == 401


@pytest.mark.negative
@pytest.mark.regression
def test_get_profile_with_malformed_auth_header():
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": "NotBearer some_random_token"
        }
    )

    assert response.status_code == 401


@pytest.mark.smoke
@pytest.mark.regression
def test_update_profile(auth_token):
    response = requests.post(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "name": "QA Test User",
            "age": 22,
            "height_cm": 170,
            "weight_kg": 65,
            "gender": "male",
            "activity_level": "sometimes",
            "goal": "maintain_weight"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, dict)

    assert "message" in response_data
    assert isinstance(response_data["message"], str)
    assert response_data["message"] == "Profile saved!"

    assert "daily_calorie_target" in response_data
    assert isinstance(
        response_data["daily_calorie_target"],
        (int, float)
    )
    assert response_data["daily_calorie_target"] > 0


@pytest.mark.negative
@pytest.mark.regression
def test_update_profile_with_unrealistic_values(auth_token):
    response = requests.post(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "name": "QA Boundary Test",
            "age": 5,
            "height_cm": 50,
            "weight_kg": 10,
            "gender": "male",
            "activity_level": "sometimes",
            "goal": "maintain_weight"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, dict)

    assert "message" in response_data
    assert isinstance(response_data["message"], str)
    assert response_data["message"] == "Profile saved!"

    assert "daily_calorie_target" in response_data
    assert isinstance(
        response_data["daily_calorie_target"],
        (int, float)
    )
    assert response_data["daily_calorie_target"] == 2000


@pytest.mark.negative
@pytest.mark.regression
def test_update_profile_without_authentication():
    response = requests.post(
        f"{BASE_URL}/profile",
        json={
            "name": "Unauthorized User",
            "age": 22,
            "height_cm": 170,
            "weight_kg": 65
        }
    )

    assert response.status_code in [401, 403]