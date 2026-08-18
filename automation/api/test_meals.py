import requests


from config import BASE_URL


def test_log_and_retrieve_meal(auth_token):
    meal_data = {
        "meal_type": "lunch",
        "food_name": "QA Test Meal",
        "calories": 450,
        "protein": 20,
        "carbs": 55,
        "fats": 12
    }

    # Step 1: Log the meal
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

    # Step 2: Retrieve today's meals
    meals_response = requests.get(
        f"{BASE_URL}/today_meals",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert meals_response.status_code == 200

    meals_data = meals_response.json()

    # Step 3: Find our test meal
    lunch_meals = meals_data["meals"]["lunch"]

    matching_meals = [
        meal
        for meal in lunch_meals
        if meal["food_name"] == "QA Test Meal"
    ]

    assert len(matching_meals) >= 1

    # Step 4: Verify the meal data
    test_meal = matching_meals[-1]

    assert test_meal["calories"] == 450
    assert test_meal["protein"] == 20
    assert test_meal["carbs"] == 55
    assert test_meal["fats"] == 12
    
def test_log_meal_missing_required_field(auth_token):
    invalid_meal_data = {
        "meal_type": "lunch",
        "food_name": "Invalid QA Meal",
        "protein": 20,
        "carbs": 55,
        "fats": 12
    }

    response = requests.post(
        f"{BASE_URL}/log_meal",
        json=invalid_meal_data,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 422