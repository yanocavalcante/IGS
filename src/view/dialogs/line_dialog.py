from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout
from models.basics.coordinate import Coordinate


class LineDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Line Coordinates")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__x1 = QLineEdit()
        self.__y1 = QLineEdit()
        self.__z1 = QLineEdit()
        self.__x2 = QLineEdit()
        self.__y2 = QLineEdit()
        self.__z2 = QLineEdit()
        form.addRow("X1:", self.__x1)
        form.addRow("Y1:", self.__y1)
        form.addRow("Z1:", self.__z1)
        form.addRow("X2:", self.__x2)
        form.addRow("Y2:", self.__y2)
        form.addRow("Z2:", self.__z2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_coords(self) -> list[list]:
        return [
            [float(self.__x1.text()), float(self.__y1.text()), float(self.__z1.text())],
            [float(self.__x2.text()), float(self.__y2.text()), float(self.__z2.text())],
        ]
