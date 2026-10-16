from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from core.coordinate import Coordinate
from core.projection import Projection


class Canvas(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.__controller = controller

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(200, 200, 200))

        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(2)
        painter.setPen(pen)

        self.draw_frame(painter)      
        self.draw_orientation_reference(painter)

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

    def draw_orientation_reference(self, painter) -> None:
        """Draws the world axes projected by the current camera orientation. Implemented using Generative AI"""
        viewport = self.__controller.viewport
        origin_x = viewport.xvpmin + 45
        origin_y = viewport.yvpmax - 45
        axis_length = 28
        axes = (
            ("X", Coordinate(1, 0, 0), QColor(220, 60, 60)),
            ("Y", Coordinate(0, 1, 0), QColor(50, 150, 70)),
            ("Z", Coordinate(0, 0, 1), QColor(60, 100, 220)),
        )

        painter.save()
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        painter.drawText(round(origin_x - 28), round(origin_y - 34), "View axes")

        for label, axis, color in axes:
            projected = Projection.parallel(axis, self.__controller.window)
            magnitude = (projected.x ** 2 + projected.y ** 2) ** 0.5
            if magnitude < 1e-9:
                continue

            end_x = origin_x + axis_length * projected.x / magnitude
            end_y = origin_y - axis_length * projected.y / magnitude
            painter.setPen(QPen(color, 2))
            painter.drawLine(round(origin_x), round(origin_y), round(end_x), round(end_y))
            painter.drawText(round(end_x + 3), round(end_y - 3), label)

        painter.restore()
