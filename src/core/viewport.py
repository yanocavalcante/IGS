from core.coordinate import Coordinate
from core.window import Window


class Viewport:
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

    def resize(self, width: float, height: float) -> None:
        self.__xvpmin = 0
        self.__yvpmin = 0
        self.__xvpmax = width
        self.__yvpmax = height

    def transform(self, coord: Coordinate, window: Window) -> Coordinate:
        xvp = self.__xvpmin + ((coord.x - window.xwmin) / window.width) * (self.__xvpmax - self.__xvpmin)
        yvp = self.__yvpmin + (1 - (coord.y - window.ywmin) / window.height) * (self.__yvpmax - self.__yvpmin)

        return Coordinate(xvp, yvp)

    def transform_all(self, coords: list[Coordinate], window: Window) -> list[Coordinate]:
        return [self.transform(c, window) for c in coords]

    def __repr__(self) -> str:
        return (f"Viewport(xvpmin={self.__xvpmin}, yvpmin={self.__yvpmin}, "
                f"xvpmax={self.__xvpmax}, yvpmax={self.__yvpmax})")
