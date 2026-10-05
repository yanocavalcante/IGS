from abc import ABC, abstractmethod
from core.coordinate import Coordinate
from models.obj_type import ObjectType
from models.basics.vertex import Vertex


class GraphicObject(ABC):
    @abstractmethod
    def __init__(self, name: str, id: int, type: ObjectType, vertexes: list[Vertex]) -> None:
        self.__name = name
        self.__id = id
        self.__type = type
        self.__vertexes = vertexes
        self.__norm_coords = vertexes
        self.__edges = []
        self.__faces = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> int:
        return self.__id

    @property
    def type(self) -> ObjectType:
        return self.__type

    @property
    def vertexes(self) -> list[Vertex]:
        return self.__vertexes

    @vertexes.setter
    def vertexes(self, vertexes):
        self.__vertexes = vertexes

    @property
    def norm_coords(self):
        return self.__norm_coords

    @norm_coords.setter
    def norm_coords(self, norm_coords):
        self.__norm_coords = norm_coords

    @property
    def edges(self):
        return self.__edges

    @property
    def faces(self):
        return self.__faces

    @abstractmethod
    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        ...

    def center(self):
        sumX = 0
        sumY = 0
        for vertex in self.vertexes:
            sumX += vertex.x
            sumY += vertex.y

        cx = sumX / len(self.vertexes)
        cy = sumY / len(self.vertexes)

        return cx, cy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__id}, name={self.__name!r})"
