import pytest
from src.Rectangle import Rectangle

def test_rectangle_area(start_api):
    r = Rectangle(side_a=3, side_b=5)
    assert r.area == 15
    #negativ
    #with pytest.raises(ValueError):
        #Rectangle(side_a=-3, side_b=5)

def test_rectangle_area_2(start_api):
    r = Rectangle(side_a=3, side_b=5)
    assert r.area == 15

@pytest.mark.skip(reason='bug')
def test_rectangle_area_3():
    r = Rectangle(side_a=3, side_b=5)
    assert r.area == 15