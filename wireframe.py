from graphic_obj import GraphicObject, ObjectType


class Wireframe(GraphicObject):
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[int]):
        super().__init__(name, id, type, coords)
