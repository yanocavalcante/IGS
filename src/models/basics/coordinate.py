from dataclasses import dataclass
from numpy import array


@dataclass
class Coordinate:
    x: float
    y: float
    z: float

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def homogeneous(self):
        return array([self.x, self.y, self.z, 1])
