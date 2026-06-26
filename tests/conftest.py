import pytest
from src.Rectangle import Rectangle
from src.Circle import Circle
from src.Square import Square
from src.Triangle import Triangle

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

@pytest.fixture
def rectangle():
    return Rectangle(5, 5)

@pytest.fixture
def circle():
    return Circle(2)

@pytest.fixture
def triangle():
    return Triangle(3, 4, 5)

@pytest.fixture
def square():
    return Square(5)
