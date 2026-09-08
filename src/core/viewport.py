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

    @property
    def width(self) -> float:
        return self.__xvpmax - self.__xvpmin

    @property
    def height(self) -> float:
        return self.__yvpmax - self.__yvpmin

    def resize(self, width: float, height: float) -> None:
        self.__xvpmin = 20
        self.__yvpmin = 20
        self.__xvpmax = width - 20
        self.__yvpmax = height - 20

    def transform(self, coord: Coordinate, window: Window) -> Coordinate:
        '''
        Since now the Viewport does not actually begins in (0,0), Xvpmin and 
        Yvpmin have to be taken into consideration when calculating the
        Viewport Transform
        '''
        xvp = (self.xvpmin + (coord.x - window.norm_xwmin) / (window.norm_xwmax - window.norm_xwmin) * self.width)
        yvp = (self.yvpmin + (1 - (coord.y - window.norm_ywmin) / (window.norm_ywmax - window.norm_ywmin)) * self.height)

        return Coordinate(xvp, yvp)

    def transform_all(self, coords: list[Coordinate], window: Window) -> list[Coordinate]:
        return [self.transform(c, window) for c in coords]

    def __repr__(self) -> str:
        return (f"Viewport(xvpmin={self.__xvpmin}, yvpmin={self.__yvpmin}, "
                f"xvpmax={self.__xvpmax}, yvpmax={self.__yvpmax})")
