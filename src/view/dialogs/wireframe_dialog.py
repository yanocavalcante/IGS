from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from core.coordinate import Coordinate


class WireframeDialog(QDialog):
    """
    Coleta uma quantidade variável de vértices para um Wireframe.

    Formato de entrada: "x1,y1; x2,y2; x3,y3" (mínimo 3 pontos).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Wireframe Coordinates")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__coords_field = QLineEdit()
        self.__coords_field.setPlaceholderText("e.g. 10,10; 50,10; 30,50")
        form.addRow("Vertices:", self.__coords_field)
        layout.addWidget(QLabel("Separe cada ponto com ';' e x,y com ','"))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.__try_accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        self.__coords: list[Coordinate] = []

    def __try_accept(self) -> None:
        try:
            coords = self.__parse(self.__coords_field.text())
            if len(coords) < 3:
                raise ValueError("Um wireframe precisa de pelo menos 3 pontos.")
            self.__coords = coords
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Entrada inválida", str(e))

    @staticmethod
    def __parse(text: str) -> list[Coordinate]:
        points = []
        for chunk in text.split(";"):
            chunk = chunk.strip()
            if not chunk:
                continue
            x_str, y_str = chunk.split(",")
            points.append(Coordinate(float(x_str), float(y_str)))
        return points

    def get_coords(self) -> list[Coordinate]:
        return self.__coords
