from core.coordinate import Coordinate
from models.obj_type import ObjectType
from .graphic_obj import GraphicObject
import numpy as np


class BezierCurve(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate]) -> None:
        super().__init__(name, id, type, coords)
        self.__control_coords = coords
        self.blending()

    @property
    def control_coords(self):
        return self.__control_coords

    @control_coords.setter
    def control_coords(self, value):
        self.__control_coords = value

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        n = len(vp_coords)

        for i in range(n-1):
            p1, p2 = vp_coords[i], vp_coords[i + 1]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))

    def blending(self):
        method_matrix_B = np.array([
            [-1,  3, -3, 1],
            [ 3, -6,  3, 0],
            [-3,  3,  0, 0],
            [ 1,  0,  0, 0]
        ])

        gbx = np.array([[coord.x] for coord in self.__control_coords])

        gby = np.array([[coord.y] for coord in self.__control_coords])

        coords = []

        for t in np.arange(0, 1.01, 0.01):
            t_vector = np.array([t**3, t**2, t, 1])

            x = t_vector @ method_matrix_B @ gbx
            y = t_vector @ method_matrix_B @ gby

            coords.append(Coordinate(x[0], y[0]))

        self.coords = coords

        return