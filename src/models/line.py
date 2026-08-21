from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class Line(GraphicObject):
    """Objeto do display file com exatamente dois pontos (segmento de reta)."""

    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate]):
        super().__init__(name, id, type, coords)

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        p1, p2 = vp_coords[0], vp_coords[1]
        painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))
