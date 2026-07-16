import pytest
import requests

DEFAULT_URL = "https://ya.ru"
DEFAULT_STATUS = 200

@pytest.fixture
def target_url(request):
    return request.config.getoption("--url")

@pytest.fixture
def expected_status(request):
    return int(request.config.getoption("--status_code"))

def test_check_status_code(target_url, expected_status):
    response = requests.get(target_url)
    assert response.status_code == expected_status
