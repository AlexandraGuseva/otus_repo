import pytest
from src.Triangle import Triangle

def test_triangle_area(start_api):
    t = Triangle(side_a=3, side_b=4, side_c=5)
    assert t.area == 6

def test_triangle_perimeter():
    t = Triangle(side_a=3, side_b=4, side_c=5)
    assert t.perimeter == 12

def test_invalid_triangle_sides():
    with pytest.raises(ValueError):
        Triangle(side_a=-1, side_b=1, side_c=10)