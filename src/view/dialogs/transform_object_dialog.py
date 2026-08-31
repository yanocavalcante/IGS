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
    QRadioButton,
    QButtonGroup,
    QLabel,
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

        self.object_center_radio = QRadioButton("Object Center")
        self.world_center_radio = QRadioButton("World Center")
        self.arbitrary_point_radio = QRadioButton("Arbitrary Point")

        self.object_center_radio.setChecked(True)

        self.rotation_group = QButtonGroup(widget)
        self.rotation_group.addButton(self.object_center_radio)
        self.rotation_group.addButton(self.world_center_radio)
        self.rotation_group.addButton(self.arbitrary_point_radio)

        layout.addWidget(QLabel("Rotation Center"))
        layout.addRow("", self.object_center_radio)
        layout.addRow("", self.world_center_radio)
        layout.addRow("", self.arbitrary_point_radio)

        self.arbitrary_x_input = QLineEdit()
        self.arbitrary_x_input.setPlaceholderText("e.g. 10")
        self.arbitrary_y_input = QLineEdit()
        self.arbitrary_y_input.setPlaceholderText("e.g. 20")

        layout.addRow("X:", self.arbitrary_x_input)
        layout.addRow("Y:", self.arbitrary_y_input)

        self.arbitrary_x_input.setEnabled(False)
        self.arbitrary_y_input.setEnabled(False)

        self.arbitrary_point_radio.toggled.connect(
            lambda checked: (
                self.arbitrary_x_input.setEnabled(checked),
                self.arbitrary_y_input.setEnabled(checked),
            )
        )

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
                if self.object_center_radio.isChecked():
                    center = "object"
                elif self.world_center_radio.isChecked():
                    center = "world"
                else:
                    center = (float(self.arbitrary_x_input.text()),
                              float(self.arbitrary_y_input.text())
                            )
                self.__result = {
                    "object": self.__current_object,
                    "operation": "rotation",
                    "angle": float(self.angle_input.text()),
                    "center": center
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
