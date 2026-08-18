import pytest
import requests

from config import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
def test_log_and_retrieve_meal(auth_token):
    meal_data = {
        "meal_type": "lunch",
        "food_name": "QA Test Meal",
        "calories": 450,
        "protein": 20,
        "carbs": 55,
        "fats": 12
    }

    log_response = requests.post(
        f"{BASE_URL}/log_meal",
        json=meal_data,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert log_response.status_code == 200

    log_data = log_response.json()

    assert log_data["message"] == "Meal logged!"
    assert "is_healthy" in log_data
    assert "alternative" in log_data

    meals_response = requests.get(
        f"{BASE_URL}/today_meals",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert meals_response.status_code == 200

    meals_data = meals_response.json()

    lunch_meals = meals_data["meals"]["lunch"]

    matching_meals = [
        meal
        for meal in lunch_meals
        if meal["food_name"] == "QA Test Meal"
    ]

    assert len(matching_meals) >= 1

    test_meal = matching_meals[-1]

    assert test_meal["calories"] == 450
    assert test_meal["protein"] == 20
    assert test_meal["carbs"] == 55
    assert test_meal["fats"] == 12




@pytest.mark.negative
@pytest.mark.regression
def test_log_meal_with_negative_calories(auth_token):
    meal_data = {
        "meal_type": "lunch",
        "food_name": "Negative Calories Test",
        "calories": -100,
        "protein": 10,
        "carbs": 20,
        "fats": 5
    }

    response = requests.post(
        f"{BASE_URL}/log_meal",
        json=meal_data,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 422

@pytest.mark.parametrize(
    "calories, expected_health",
    [
        (0, "yes"),
        (100, "yes"),
        (400, "yes"),
        (699, "yes"),
        (700, "yes"),
        (701, "no"),
        (800, "no"),
        (1000, "no"),
    ],
)
@pytest.mark.regression
def test_log_meal_calorie_boundaries(
    auth_token,
    calories,
    expected_health
):
    meal_data = {
        "meal_type": "lunch",
        "food_name": f"Parameterized {calories} Calories Test",
        "calories": calories,
        "protein": 20,
        "carbs": 50,
        "fats": 10
    }

    response = requests.post(
        f"{BASE_URL}/log_meal",
        json=meal_data,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["message"] == "Meal logged!"
    assert response_data["is_healthy"] == expected_health

    if expected_health == "no":
        assert response_data["alternative"] is not None
    else:
        assert response_data["alternative"] is None


@pytest.mark.negative
@pytest.mark.regression
def test_log_meal_without_authentication():
    meal_data = {
        "meal_type": "lunch",
        "food_name": "Unauthorized Meal",
        "calories": 450,
        "protein": 20,
        "carbs": 55,
        "fats": 12
    }

    response = requests.post(
        f"{BASE_URL}/log_meal",
        json=meal_data
    )

    assert response.status_code in [401, 403]
