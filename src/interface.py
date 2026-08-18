from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QInputDialog,
)


class SGIInterface(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Interactive Graphic System')
        self.setGeometry(100, 100, 1024, 768)

        self.display_file = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.create_menu()
        self.create_viewport()

    def create_viewport(self):
        self.viewport = QWidget()
        self.viewport_layout = QVBoxLayout()
        self.viewport.setLayout(self.viewport_layout)
        self.main_layout.addWidget(self.viewport, 4)

    def create_menu(self):
        self.menu = QWidget()
        self.menu_layout = QVBoxLayout(self.menu)

        self.main_layout.addWidget(self.menu, 1)

        self.menu_layout.addWidget(QLabel("Zoom"))
        self.zoom_layout = QGridLayout()

        self.add_menu_button(
            self.zoom_layout,
            "Zoom +",
            self.zoom_in,
            0, 0
        )

        self.add_menu_button(
            self.zoom_layout,
            "Zoom -",
            self.zoom_out,
            0, 1
        )

        self.menu_layout.addLayout(self.zoom_layout)

        self.menu_layout.addWidget(QLabel("Navigation"))
        self.navigation_layout = QGridLayout()

        self.add_menu_button(
            self.navigation_layout,
            "Up",
            self.move_up,
            1, 1
        )

        self.add_menu_button(
            self.navigation_layout,
            "Left",
            self.move_left,
            2, 0
        )

        self.add_menu_button(
            self.navigation_layout,
            "Down",
            self.move_down,
            2, 1
        )

        self.add_menu_button(
            self.navigation_layout,
            "Right",
            self.move_right,
            2, 2
        )

        self.menu_layout.addLayout(self.navigation_layout)

        self.menu_layout.addWidget(QLabel("Objects"))
        self.objects_layout = QGridLayout()

        self.add_menu_button(
            self.objects_layout,
            "Create New Object",
            self.create_object,
            0, 0
        )

        self.menu_layout.addLayout(self.objects_layout)
        self.menu_layout.addStretch()

    def add_menu_button(self, layout, text, callback, row, column):
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button, row, column)

    def zoom_in(self):
        QMessageBox.information(self, "IGS", "You zoomed in!")

    def zoom_out(self):
        QMessageBox.information(self, "IGS", "You zoomed out!")

    def move_up(self):
        QMessageBox.information(self, "IGS", "You moved up!")

    def move_down(self):
        QMessageBox.information(self, "IGS", "You moved down!")

    def move_left(self):
        QMessageBox.information(self, "IGS", "You moved left!")

    def move_right(self):
        QMessageBox.information(self, "IGS", "You moved right!")

    def create_object(self):
        object_dict = {"Name": "", "Type": "", "Coords": ""}
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Object")

        dialog_layout = QVBoxLayout(dialog)
        dialog_form_layout = QFormLayout()

        name = QLineEdit()
        name.setPlaceholderText("e.g. MyFirstObject")

        coords = QLineEdit()
        coords.setPlaceholderText("e.g. (1,1),(2,2),(4,4)")

        dialog_form_layout.addRow("Name:", name)

        obj_type = QComboBox()
        obj_type.setPlaceholderText("Object Type")
        obj_type.addItems([
            "Point",
            "Line",
            "Polygon"
        ])
        dialog_form_layout.addWidget(obj_type)

        dialog_form_layout.addRow("Coords:", coords)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Ok
        )

        dialog_layout.addLayout(dialog_form_layout)

        dialog_layout.addWidget(button_box)

        button_box.rejected.connect(dialog.reject)
        button_box.accepted.connect(dialog.accept)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            object_dict["Name"] = name.text()
            object_dict["Type"] = obj_type.currentText()
            object_dict["Coords"] = coords.text()

            print(object_dict) # For testing - Remove

            return object_dict

    def open_input_dialog(self):
        name, ok = QInputDialog.getText(
            self,
            'Name',
            'Name:'
        )

        if ok and name:
            self.setWindowTitle(name)