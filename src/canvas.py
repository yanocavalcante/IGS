from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen


class Canvas(QWidget):
    def __init__(self, display_file):
        super().__init__()
        self.__display_file = display_file

    def paintEvent(self, event):
        '''
        This method is called by Qt itself everytime the Widget
        needs to be drawn or redrawn, for instance, the first
        time it is instantiated or when widget.update() is called
        '''
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(200, 200, 200))
        self.hi(painter) # This is a test
        for obj in self.__display_file:
            self.draw_object(painter, obj)

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

    def draw_object(self, painter, literal_object):
        pen = QPen(QColor(200, 0, 0))
        pen.setWidth(4)
        painter.setPen(pen)
        literal_object.draw(painter)

    def draw_grid(self):
        pass