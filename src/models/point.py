from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class Point(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate]):
        super().__init__(name, id, type, coords)

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        p = vp_coords[0]
        painter.drawPoint(round(p.x), round(p.y))
