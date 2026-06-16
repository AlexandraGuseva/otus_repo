from src.Rectangle import Rectangle

class Square(Rectangle):
    def __init__(self, side_a: int or float):
        if side_a <= 0:
            raise ValueError("side_a must be positive")

        super().__init__(side_a, side_a)
        self.side_a = self.side_a


s = Square(5)
print(s.area)
print(s.perimeter)
