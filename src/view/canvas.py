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

        for obj, vp_coords in self.__controller.get_drawable_objects():
            obj.draw(painter, vp_coords)
