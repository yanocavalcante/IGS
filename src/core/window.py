from models.basics.coordinate import Coordinate
from models.basics.vertex import Vertex
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType
import numpy as np


class Window(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, vertexes: list[Vertex]) -> None:
        super().__init__(name, id, type, vertexes)

        self.__theta_y = 0
        self.__theta_x = 0

        self.__norm_xwmin = -1
        self.__norm_ywmin = -1
        self.__norm_xwmax = 1
        self.__norm_ywmax = 1

    @property
    def xwmin(self) -> float:
        return self.vertexes[0].coordinate.x

    @property
    def ywmin(self) -> float:
        return self.vertexes[0].coordinate.y

    @property
    def zwmin(self) -> float:
        return self.vertexes[0].coordinate.z

    @property
    def xwmax(self) -> float:
        return self.vertexes[2].coordinate.x    

    @property
    def ywmax(self) -> float:
        return self.vertexes[2].coordinate.y

    @property
    def zwmax(self) -> float:
        return self.vertexes[2].coordinate.z    

    @property
    def norm_xwmin(self) -> float:
        return self.__norm_xwmin

    @property
    def norm_ywmin(self) -> float:
        return self.__norm_ywmin

    @property
    def norm_xwmax(self) -> float:
        return self.__norm_xwmax

    @property
    def norm_ywmax(self) -> float:
        return self.__norm_ywmax
      
    @property
    def width(self) -> float:
        return self.xwmax - self.xwmin

    @property
    def height(self) -> float:
        return self.ywmax - self.ywmin

    @property
    def center(self) -> Vertex:
        return Vertex(Coordinate((self.xwmin + self.xwmax)/2,
                                  (self.ywmin + self.ywmax)/2,
                                    (self.zwmin + self.zwmax)/2))

    @property
    def theta_x(self) -> float:
        return self.__theta_x

    @theta_x.setter
    def theta_x(self, value):
        self.__theta_x = value

    @property
    def theta_y(self) -> float:
        return self.__theta_y

    @theta_y.setter
    def theta_y(self, value):
        self.__theta_y = value

    @property
    def vup(self):
        theta_y = self.theta_y * (np.pi/180)

        return np.array([
            np.sin(theta_y),
             np.cos(theta_y)
        ])

    @property
    def vright(self):
        theta_y = self.theta_y * (np.pi/180)

        return np.array([
            np.cos(theta_y),
              -np.sin(theta_y)
        ])

    def pan(self, dx: float, dy: float, dz: float) -> None:
        movement = dx * self.vright + dy * self.vup

        for vertex in self.vertexes:
            vertex.coordinate.x += movement[0]
            vertex.coordinate.y += movement[1]

    def zoom(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("Zoom factor must be greater than zero")

        center = self.center

        for vertex in self.vertexes:
            vertex.coordinate.x = center.coordinate.x + (vertex.coordinate.x - center.coordinate.x) * factor
            vertex.coordinate.y = center.coordinate.y + (vertex.coordinate.y - center.coordinate.y) * factor

    def rotate(self, angle: float) -> None:
        self.theta_y = (self.theta_y + angle) % 360

    def match_aspect_ratio(self, aspect_ratio: float) -> None:
        if aspect_ratio <= 0:
            raise ValueError("Aspect ratio must be greater than zero")

        center = self.center

        half_height = self.height / 2
        half_width = half_height * aspect_ratio

        self.vertexes[0].coordinate.x = center.coordinate.x - half_width
        self.vertexes[1].coordinate.x = center.coordinate.x - half_width
        self.vertexes[2].coordinate.x = center.coordinate.x + half_width
        self.vertexes[3].coordinate.x = center.coordinate.x + half_width

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        return 