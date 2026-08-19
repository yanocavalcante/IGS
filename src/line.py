from graphic_obj import GraphicObject, ObjectType


class Line(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[int]):
        super().__init__(name, id, type, coords)

    def draw(self, painter):
        painter.drawLine(self.coords[0], self.coords[1],
                         self.coords[2], self.coords[3])

    def transform(self):
        pass
