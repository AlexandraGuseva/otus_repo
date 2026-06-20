import pytest
import math
from src.Circle import Circle

def test_circle_area():
    c = Circle(5)
    assert c.area == pytest.approx(math.pi*(5**2))

def test_circle_perimeter():
    c = Circle(5)
    assert c.perimeter == pytest.approx(2*math.pi*5)

@pytest.mark.parametrize("negative_radius", [-5, -1, 0])
def test_circle_negative_radius(negative_radius):
    with pytest.raises(ValueError, match="radius must be positive"):
        Circle(negative_radius)

