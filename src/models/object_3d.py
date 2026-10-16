from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class Object3D(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate], edges: list[tuple[int, int]]):
        if len(coords) < 2:
            raise ValueError("A 3D object needs at least two vertices.")
        if not edges:
            raise ValueError("A 3D object needs at least one edge.")

        super().__init__(name, id, type, coords)
        self.__edges = edges
        self.__visible_edges: list[list[Coordinate]] = []

    @property
    def edges(self) -> list[tuple[int, int]]:
        return self.__edges

    @property
    def visible_edges(self) -> list[list[Coordinate]]:
        return self.__visible_edges

    @visible_edges.setter
    def visible_edges(self, value: list[list[Coordinate]]) -> None:
        self.__visible_edges = value

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        for p1, p2 in self.__visible_edges:
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))
