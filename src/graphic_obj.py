from abc import ABC, abstractmethod
from obj_type import ObjectType


class GraphicObject(ABC):
    @abstractmethod
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[int]) -> None:
        self.__name = name
        self.__id = id
        self.__type = type
        self.__coords = coords

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
    def coords(self) -> list[int]:
        return self.__coords
