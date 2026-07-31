import pytest
import json
import requests
from faker import Faker

@pytest.mark.api_1

def test_public_v2_users():
    url = 'https://gorest.co.in/public/v2/users'

    response = requests.get(url)

    assert response.status_code == 200

    user = {
    "id": 8515333,
    "name": "Manoj Guha",
    "email": "manoj_guha@murray.test",
    "gender": "male",
    "status": "active",
    }
    response_json = response.json()
    breakpoint()
    assert isinstance(response_json, list)
    assert response_json[0] == user


