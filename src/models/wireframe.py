from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class Wireframe(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate],
                 closed: bool = True):
        super().__init__(name, id, type, coords)
        self.__closed = closed

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        n = len(vp_coords)
        if n < 2:
            return

        for i in range(n - 1):
            p1, p2 = vp_coords[i], vp_coords[i + 1]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))

        if self.__closed and n > 2:
            p1, p2 = vp_coords[-1], vp_coords[0]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))
