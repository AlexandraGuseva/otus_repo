import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

def test_get_all_breweries():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data)>0

@pytest.mark.parametrize("city", ["boulder city", "austintown", "southportland"])
def test_filter_by_city(city):
    response = requests.get(f'{BASE_URL}?by_city={city}')
    assert response.status_code == 200
    data = response.json()

    if len(data)>0:
        for brewery in data:
            assert brewery['city'].lower() == city.lower()

@pytest.mark.parametrize("brewery_type", ["micro", "regional", "brewpub"])
def test_filter_by_brewery_type(brewery_type):
    response = requests.get(f"{BASE_URL}?by_type={brewery_type}")
    assert response.status_code == 200
    data = response.json()

    if len(data)>0:
        for brewery in data:
            assert brewery['brewery_type'] == brewery_type

def test_breweries_have_required_fields():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()

    required_fields = ['id', 'name', 'brewery_type', 'city', 'state', 'country']
    for brewery in data[:5]:
        for field in required_fields:
            assert field in brewery

def test_limit_results():
    limit=3
    response = requests.get(f"{BASE_URL}?per_page={limit}")
    assert response.status_code == 200
    data = response.json()
    assert len(data)>=limit