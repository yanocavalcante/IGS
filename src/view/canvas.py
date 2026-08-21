from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class Canvas(QWidget):
    """
    O dispositivo de saída físico (seção 1.4 -- "Display Rectangle").

    Não guarda display_file próprio e não sabe nada sobre Window ou
    Viewport: a cada repintura, pergunta ao Controller o que desenhar
    (já em coordenadas de tela) e apenas pinta. O corte visual de
    objetos parcialmente fora da área (seção 1.9, clipping) é feito
    automaticamente pelo QPainter nos limites do widget.
    """

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
