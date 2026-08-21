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
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Wireframe Coordinates")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__coords_field = QLineEdit()
        self.__coords_field.setPlaceholderText("e.g. 10,10; 50,10; 30,50")
        form.addRow("Vertices:", self.__coords_field)
        layout.addWidget(QLabel("Input different points using ';' and x, y coordinates with ','"))

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
                raise ValueError("A wireframe needs, at least, 3 points.")
            self.__coords = coords
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid input", str(e))

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
