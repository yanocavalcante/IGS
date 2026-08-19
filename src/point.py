from graphic_obj import GraphicObject, ObjectType


class Point(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[int]):
        super().__init__(name, id, type, coords)

    def draw(self, painter):
        painter.drawPoint(self.coords[0], self.coords[1])

    def transform(self):
        pass