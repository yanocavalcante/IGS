class Window:
    def __init__(self, xwmin: float, ywmin: float, xwmax: float, ywmax: float) -> None:
        self.__xwmin = xwmin
        self.__ywmin = ywmin
        self.__xwmax = xwmax
        self.__ywmax = ywmax

    @property
    def xwmin(self) -> float:
        return self.__xwmin

    @property
    def ywmin(self) -> float:
        return self.__ywmin

    @property
    def xwmax(self) -> float:
        return self.__xwmax

    @property
    def ywmax(self) -> float:
        return self.__ywmax

    @property
    def width(self) -> float:
        return self.__xwmax - self.__xwmin

    @property
    def height(self) -> float:
        return self.__ywmax - self.__ywmin

    def pan(self, dx: float, dy: float) -> None:
        """
        Move a window no mundo (navegação).

        TODO: implementar. Deve deslocar xwmin/ywmin/xwmax/ywmax por
        (dx, dy), mantendo a largura e altura da window inalteradas.
        """
        raise NotImplementedError

    def zoom(self, factor: float) -> None:
        """
        Redimensiona a window (zoom in/out).

        TODO: implementar. factor > 1 deve aumentar a window (zoom out,
        vê mais mundo); factor < 1 deve diminuí-la (zoom in). Pense em
        como manter o centro da window fixo durante a operação.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return (f"Window(xwmin={self.__xwmin:.1f}, ywmin={self.__ywmin:.1f}, "
                f"xwmax={self.__xwmax:.1f}, ywmax={self.__ywmax:.1f})")
