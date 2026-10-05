from dataclasses import dataclass
from core.coordinate import Coordinate


@dataclass
class Vertex:
    coordinate: Coordinate

    @property
    def x(self):
        return self.coordinate.x

    @property
    def y(self):
        return self.coordinate.y

    @property
    def z(self):
        return self.coordinate.z

    def homogeneous(self):
        return self.coordinate.homogeneous()
