import pytest

from src.Rectangle import Rectangle


@pytest.fixture(scope='session')
def start_db():
    print("\nSTART DB")

    yield

    print("\nSTOP DB")


@pytest.fixture(scope='session')
def start_api(start_db):
    print("\nSTART API")

    yield

    print("\nSTOP API")
