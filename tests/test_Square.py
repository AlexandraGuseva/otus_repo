import pytest
from src.Square import Square

def test_square_area(start_api):
    s = Square(side_a=4)
    assert s.area == 16

def test_square_perimeter():
    s = Square(side_a=4)
    assert s.perimeter == 16

def test_square_negative_side():
    with pytest.raises(ValueError):
        Square(side_a=-1)