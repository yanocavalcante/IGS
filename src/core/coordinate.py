from dataclasses import dataclass
from numpy import array


@dataclass
class Coordinate:
    x: float
    y: float

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

    def homogeneous(self):
        return array([self.x, self.y, 1])
