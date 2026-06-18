from src.Figure import Figure

class Rectangle(Figure):
    def __init__(self, side_a: (int or float), side_b: (int or float)):
        if side_a <= 0 or side_b <= 0:
            raise ValueError("side_a and side_b must be positive")
        self.side_a = side_a
        self.side_b = side_b

    @property
    def perimeter(self):
        return (self.side_a + self.side_b) * 2

    @property
    def area(self):
        return self.side_a * self.side_b


if __name__ == "__main__":
    r = Rectangle(3, 5)
    print(r.side_a)
    print(r.side_b)
    print(r.perimeter)
    print(r.area)

