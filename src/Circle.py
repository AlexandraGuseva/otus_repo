import math
from src.Figure import Figure

class Circle(Figure):

    def __init__(self, radius: (int or float)):
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius

    @property
    def perimeter(self):
        # Периметр круга — это длина его окружности (2 * pi * r)
        return 2 * math.pi * self.radius

    @property
    def area(self):
        # Площадь круга (pi * r^2)
        return math.pi * (self.radius ** 2)

if __name__ == "__main__":
    c = Circle(5)
    print(c.radius)
    print(c.perimeter)
    print(c.area)