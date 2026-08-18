from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
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
        self.main_layout.addWidget(self.viewport)

    def create_menu(self):
        self.menu = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu.setLayout(self.menu_layout)
        self.main_layout.addWidget(self.menu)

        zoomIn_btn = QPushButton('Zoom +')
        zoomIn_btn.clicked.connect(self.zoom_in)
        self.menu_layout.addWidget(zoomIn_btn)

        zoomOut_btn = QPushButton('Zoom -')
        zoomOut_btn.clicked.connect(self.zoom_out)
        self.menu_layout.addWidget(zoomOut_btn)

        moveUp_btn = QPushButton('Up')
        moveUp_btn.clicked.connect(self.move_up)
        self.menu_layout.addWidget(moveUp_btn)

        moveDown_btn = QPushButton('Down')
        moveDown_btn.clicked.connect(self.move_down)
        self.menu_layout.addWidget(moveDown_btn)

        moveLeft_btn = QPushButton('Left')
        moveLeft_btn.clicked.connect(self.move_left)
        self.menu_layout.addWidget(moveLeft_btn)

        moveRight_btn = QPushButton('Right')
        moveRight_btn.clicked.connect(self.move_right)
        self.menu_layout.addWidget(moveRight_btn)

        create_btn = QPushButton('Create New Object')
        create_btn.clicked.connect(self.create_object)
        self.menu_layout.addWidget(create_btn)

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
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Object")

        dialog_layout = QVBoxLayout(dialog)
        dialog_form_layout = QFormLayout()

        name = QLineEdit()
        object_type = QComboBox()

        object_type.addItems([
            "Point",
            "Line",
            "Polygon"
        ])

        coords_widget = QWidget()
        coords_layout = QFormLayout(coords_widget)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        dialog_form_layout.addRow("Name:", name)
        dialog_form_layout.addRow("Type:", object_type)

        dialog_layout.addLayout(dialog_form_layout)
        dialog_layout.addWidget(coords_widget)
        dialog_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog.exec()

    def open_input_dialog(self):
        name, ok = QInputDialog.getText(
            self,
            'Name',
            'Name:'
        )

        if ok and name:
            self.setWindowTitle(name)