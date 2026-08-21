from abc import ABC, abstractmethod

from core.coordinate import Coordinate
from models.obj_type import ObjectType


class GraphicObject(ABC):
    """
    Representa um item do Display File (seção 1.9 do material).

    Guarda dados em coordenadas de MUNDO e sabe desenhar a si mesmo
    -- mas apenas quando já recebe as coordenadas transformadas para
    tela (vp_coords). Não conhece Window nem Viewport: quem faz a
    transformação é o Controller, via Viewport.transform_all().
    """

    @abstractmethod
    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate]) -> None:
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
    def coords(self) -> list[Coordinate]:
        return self.__coords

    @abstractmethod
    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        """
        Desenha o objeto usando coordenadas JÁ transformadas para o
        espaço de tela (vp_coords). Não deve usar self.coords
        diretamente para desenhar -- self.coords é sempre mundo.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__id}, name={self.__name!r})"
