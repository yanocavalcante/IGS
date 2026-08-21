from core.coordinate import Coordinate
from core.window import Window


class Viewport:
    """
    Retângulo em coordenadas de TELA para onde a Window é mapeada
    (seção 1.11 do material -- Transformada de Viewport).

    É uma função de mapeamento pura: dado um ponto de mundo e a
    Window atual, calcula o ponto correspondente em coordenadas de
    tela. Não guarda estado de nenhum objeto específico, não desenha
    nada -- só faz a conta (EQ. 1.1 / 1.2).
    """

    def __init__(self, xvpmin: float, yvpmin: float, xvpmax: float, yvpmax: float) -> None:
        self.__xvpmin = xvpmin
        self.__yvpmin = yvpmin
        self.__xvpmax = xvpmax
        self.__yvpmax = yvpmax

    @property
    def xvpmin(self) -> float:
        return self.__xvpmin

    @property
    def yvpmin(self) -> float:
        return self.__yvpmin

    @property
    def xvpmax(self) -> float:
        return self.__xvpmax

    @property
    def yvpmax(self) -> float:
        return self.__yvpmax

    def transform(self, coord: Coordinate, window: Window) -> Coordinate:
        """
        Mapeia um único ponto de coordenadas de mundo (segundo a Window
        atual) para coordenadas de tela (dentro deste Viewport).
        Implementa a EQ. 1.1 e a inversão do eixo Y da seção 1.11.
        """
        xvp = ((coord.x - window.xwmin) / window.width) * (self.__xvpmax - self.__xvpmin)
        yvp = (1 - (coord.y - window.ywmin) / window.height) * (self.__yvpmax - self.__yvpmin)
        return Coordinate(xvp, yvp)

    def transform_all(self, coords: list[Coordinate], window: Window) -> list[Coordinate]:
        """Aplica transform() em uma lista inteira de coordenadas de mundo."""
        return [self.transform(c, window) for c in coords]

    def __repr__(self) -> str:
        return (f"Viewport(xvpmin={self.__xvpmin}, yvpmin={self.__yvpmin}, "
                f"xvpmax={self.__xvpmax}, yvpmax={self.__yvpmax})")
