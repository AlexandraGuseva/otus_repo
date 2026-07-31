import pytest
import requests

BASE_URL = "https://dog.ceo/api"

def test_get_all_breeds():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert isinstance(data['message'], dict)
    assert len(data['message']) > 0

def test_get_random_dog_image():
    response = requests.get(f"{BASE_URL}/breeds/image/random")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert data['message'].endswith('.jpg')

@pytest.mark.parametrize("breed", [
    "hound",
    "beagle",
    "bulldog"
])
def test_get_breed_images(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert len(data['message'])>0

@pytest.mark.parametrize("breed,expected_subbreeds", [
    ("hound", ["afgan", "basset", "blood", "english", "ibizan"]),
    ("bulldog", ["boston", "english", "french"])
])
def test_get_subbreeds(breed, expected_subbreeds):
    response = requests.get(f"{BASE_URL}/breed/{breed}/list")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert set(data['message']) == set(expected_subbreeds)

def test_get_random_image_by_breed():
    breed = "hound"
    response = requests.get(f"{BASE_URL}/breed/{breed}/images/random")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert f'{breed}' in data['message']

def test_invalid_breed():
    response = requests.get(f"{BASE_URL}/breed/invalid/images")
    assert response.status_code == 404
    data = response.json()
    assert data['status'] == 'error'

