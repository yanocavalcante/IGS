from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class TransformObjectDialog(QDialog):
    def __init__(self, current_object, parent=None) -> None:
        super().__init__(parent)
        self.__current_object = current_object
        self.__result: dict | None = None

        self.setWindowTitle("Transform Object")

        layout = QVBoxLayout(self)

        self.operation_selector = QComboBox()
        self.operation_selector.addItems([
            "Translation",
            "Rotation",
            "Scaling"
        ])

        layout.addWidget(self.operation_selector)

        self.stack = QStackedWidget()

        self.stack.addWidget(self.translation())
        self.stack.addWidget(self.rotation())
        self.stack.addWidget(self.scaling())

        layout.addWidget(self.stack)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.operation_selector.currentIndexChanged.connect(
            self.stack.setCurrentIndex
        )

    def translation(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)

        self.dx_input = QLineEdit()
        self.dy_input = QLineEdit()
        self.dx_input.setPlaceholderText("e.g. 20")
        self.dy_input.setPlaceholderText("e.g. -10")

        layout.addRow("DX:", self.dx_input)
        layout.addRow("DY:", self.dy_input)

        return widget

    def rotation(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("e.g. 45°")

        layout.addRow("Angle:", self.angle_input)

        return widget

    def scaling(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)

        self.sx_input = QLineEdit()
        self.sy_input = QLineEdit()
        self.sx_input.setPlaceholderText("e.g. 2.0")
        self.sy_input.setPlaceholderText("e.g. 1.5")

        layout.addRow("SX:", self.sx_input)
        layout.addRow("SY:", self.sy_input)

        return widget

    def get_object_transformation_dict(self) -> dict | None:
        if self.exec() != QDialog.DialogCode.Accepted:
            return None

        return self.__result

    def accept(self) -> None:
        operation = self.operation_selector.currentText()

        try:
            if operation == "Translation":
                self.__result = {
                    "object": self.__current_object,
                    "operation": "translation",
                    "dx": float(self.dx_input.text()),
                    "dy": float(self.dy_input.text()),
                }

            elif operation == "Rotation":
                self.__result = {
                    "object": self.__current_object,
                    "operation": "rotation",
                    "angle": float(self.angle_input.text()),
                }

            elif operation == "Scaling":
                self.__result = {
                    "object": self.__current_object,
                    "operation": "scaling",
                    "sx": float(self.sx_input.text()),
                    "sy": float(self.sy_input.text()),
                }

            super().accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Fill all fields with valid numbers.")
