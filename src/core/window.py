class Window:
    def __init__(self, xwmin: float, ywmin: float, xwmax: float, ywmax: float) -> None:
        self.__xwmin = xwmin
        self.__ywmin = ywmin
        self.__xwmax = xwmax
        self.__ywmax = ywmax

    @property
    def xwmin(self) -> float:
        return self.__xwmin

    @xwmin.setter
    def xwmin(self, value):
        self.__xwmin = value        

    @property
    def ywmin(self) -> float:
        return self.__ywmin

    @ywmin.setter
    def ywmin(self, value):
        self.__ywmin = value        

    @property
    def xwmax(self) -> float:
        return self.__xwmax

    @xwmax.setter
    def xwmax(self, value):
        self.__xwmax = value        

    @property
    def ywmax(self) -> float:
        return self.__ywmax

    @ywmax.setter
    def ywmax(self, value):
        self.__ywmax = value        

    @property
    def width(self) -> float:
        return self.__xwmax - self.__xwmin

    @property
    def height(self) -> float:
        return self.__ywmax - self.__ywmin

    def pan(self, dx: float, dy: float) -> None:
        self.xwmin += dx
        self.xwmax += dx
        self.ywmin += dy
        self.ywmax += dy

    def zoom(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("Zoom factor must be greater than zero")

        center_x = (self.__xwmin + self.__xwmax) / 2
        center_y = (self.__ywmin + self.__ywmax) / 2
        half_width = (self.width * factor) / 2
        half_height = (self.height * factor) / 2

        self.__xwmin = center_x - half_width
        self.__xwmax = center_x + half_width
        self.__ywmin = center_y - half_height
        self.__ywmax = center_y + half_height

    def __repr__(self) -> str:
        return (f"Window(xwmin={self.__xwmin:.1f}, ywmin={self.__ywmin:.1f}, "
                f"xwmax={self.__xwmax:.1f}, ywmax={self.__ywmax:.1f})")
