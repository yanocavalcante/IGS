from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class Canvas(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.__controller = controller

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(200, 200, 200))

        pen = QPen(QColor(200, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        self.draw_frame(painter)      

        for obj, vp_coords in self.__controller.get_drawable_objects():
            obj.draw(painter, vp_coords)

    def resizeEvent(self, event) -> None:
        self.__controller.resize_viewport(self.width(), self.height())
        super().resizeEvent(event)

    def draw_frame(self, painter):
        painter.drawLine(int(self.__controller.viewport.xvpmin),
         int(self.__controller.viewport.yvpmin),
           int(self.__controller.viewport.xvpmax),
             int(self.__controller.viewport.yvpmin))

        painter.drawLine(int(self.__controller.viewport.xvpmax),
         int(self.__controller.viewport.yvpmin),
           int(self.__controller.viewport.xvpmax),
             int(self.__controller.viewport.yvpmax))

        painter.drawLine(int(self.__controller.viewport.xvpmax),
         int(self.__controller.viewport.yvpmax),
           int(self.__controller.viewport.xvpmin),
             int(self.__controller.viewport.yvpmax))
        
        painter.drawLine(int(self.__controller.viewport.xvpmin),
         int(self.__controller.viewport.yvpmax),
           int(self.__controller.viewport.xvpmin),
             int(self.__controller.viewport.yvpmin))