from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(200, 200, 200))
        self.hi(painter) # This is a test

    def hi(self, painter):
        # Completely Random Valuess
        pen = QPen(QColor(200, 0, 0))
        pen.setWidth(4)
        painter.setPen(pen)

        painter.drawLine(50, 50,
                          50, 350)
        painter.drawLine(50, 200,
                          150, 200)
        painter.drawLine(150, 50,
                          150, 350)

        painter.drawLine(200, 50,
                          200, 75)
        painter.drawLine(200, 100,
                          200, 350)
        
        painter.drawLine(250, 50,
                          250, 300)
        painter.drawLine(250, 325,
                          250, 350)


    def draw_grid(self):
        pass