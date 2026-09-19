from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType
from PyQt6.QtGui import QPolygonF, QBrush
from PyQt6.QtCore import QPointF, Qt


class Wireframe(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate],
                 closed: bool = True, filled: bool = False):
        super().__init__(name, id, type, coords)
        self.__closed = closed
        self.__filled = filled

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        n = len(vp_coords)
        if n < 2:
            return

        painter.setBrush(QBrush(Qt.GlobalColor.red))

        polygon = QPolygonF( QPointF(p.x, p.y) for p in vp_coords)

        if self.__filled and self.__closed and n > 2:
            painter.drawPolygon(polygon)

        for i in range(n - 1):
            p1, p2 = vp_coords[i], vp_coords[i + 1]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))

        if self.__closed and n > 2:
            p1, p2 = vp_coords[-1], vp_coords[0]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))
