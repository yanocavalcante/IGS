from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout


class PointDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Point Coordinates")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__x = QLineEdit()
        self.__y = QLineEdit()
        self.__z = QLineEdit()
        form.addRow("X:", self.__x)
        form.addRow("Y:", self.__y)
        form.addRow("Z:", self.__z)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_coords(self) -> list[list]:
        return [[float(self.__x.text()), float(self.__y.text()), float(self.__z.text())]]
