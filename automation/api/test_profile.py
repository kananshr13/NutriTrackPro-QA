import requests


from config import BASE_URL


def test_get_profile(auth_token):
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    profile_data = response.json()

    assert profile_data is not None
def test_get_profile_without_authentication():
    response = requests.get(
        f"{BASE_URL}/profile"
    )

    assert response.status_code in [401, 403]