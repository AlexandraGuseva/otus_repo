import pytest
from src.Figure import Figure
from src.Circle import Circle
from src.Rectangle import Rectangle

def test_add_area_success():
    c=Circle(5)
    r=Rectangle(3,4)
    result = r.add_area(c)
    assert result == pytest.approx(r.area+c.area)

def test_add_area_invalid_arguments():
    r=Rectangle(3,4)
    with pytest.raises(ValueError, match="Argument figure must be Figure or child class"):
        r.add_area("blabla")