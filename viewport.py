class Viewport:
    def __init__(self, xvpmin, yvpmin, xvpmax, yvpmax) -> None:
        self.__xvpmin = xvpmin
        self.__yvpmin = yvpmin
        self.__xvpmax = xvpmax
        self.__yvpmax = yvpmax

    def transform(self, window):
        self.__xvp = ((window.xw - window.xwmin) / (window.xwmax - window.xwmin)) * (self.__xvpmax - self.__xvpmin)
        self.__yvp = ((1 - (window.yw - window.ywmin)) / (window.ywmax - window.ywmin)) * (self.__yvpmax - self.__yvpmin)

    @property
    def xvp(self):
        return self.__xvp

    @property
    def yvp(self):
        return self.__yvp