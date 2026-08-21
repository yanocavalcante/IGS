from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class DisplayFile:
    def __init__(self) -> None:
        self.__objects: list[GraphicObject] = []
        self.__next_id: int = 1

    def add(self, obj_class: type[GraphicObject], obj_type: ObjectType, name: str, coords: list[Coordinate]) -> GraphicObject:
        obj = obj_class(name, self.__next_id, obj_type, coords)
        self.__next_id += 1
        self.__objects.append(obj)

        return obj

    def remove(self, obj_id: int) -> bool:
        for i, obj in enumerate(self.__objects):
            if obj.id == obj_id:
                del self.__objects[i]

                return True

        return False

    def get_by_id(self, obj_id: int) -> GraphicObject | None:
        return next((obj for obj in self.__objects if obj.id == obj_id), None)

    def get_by_name(self, name: str) -> GraphicObject | None:
        return next((obj for obj in self.__objects if obj.name == name), None)

    @property
    def objects(self) -> list[GraphicObject]:
        return self.__objects

    def __len__(self) -> int:
        return len(self.__objects)

    def __iter__(self):
        return iter(self.__objects)
