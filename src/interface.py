from canvas import Canvas
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
    def __init__(self, controller):
        super().__init__()
        self.__controller = controller
        self.setWindowTitle('Interactive Graphic System')
        self.setGeometry(100, 100, 1024, 768)

        self.display_file = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.create_menu()
        self.create_canvas()

    def create_canvas(self):
        self.canvas = Canvas(self.display_file)
        self.canvas_layout = QVBoxLayout()
        self.canvas.setLayout(self.canvas_layout)
        self.main_layout.addWidget(self.canvas, 4)

    # def create_viewport(self):
    #     self.viewport = QWidget()
    #     self.viewport_layout = QVBoxLayout()
    #     self.viewport.setLayout(self.viewport_layout)
    #     self.main_layout.addWidget(self.viewport, 4)

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
        object_dict = {"Name": "", "Type": "", "Coords": []}
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
            "Wireframe"
        ])

        dialog_form_layout.addWidget(obj_type)

        # dialog_form_layout.addRow("Coords:", coords)

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
            match obj_type.currentText():
                case "Point":
                    point_dialog = QDialog(self)
                    point_dialog.setWindowTitle("Point Coordinates")
                    point_dialog_layout = QVBoxLayout(point_dialog)
                    point_dialog_form_layout = QFormLayout()
                    x = QLineEdit()
                    point_dialog_form_layout.addRow("X:", x)
                    y = QLineEdit()
                    point_dialog_form_layout.addRow("Y:", y)
                    point_button_box = QDialogButtonBox(
                        QDialogButtonBox.StandardButton.Cancel |
                        QDialogButtonBox.StandardButton.Ok
                    )
                    point_dialog_layout.addLayout(point_dialog_form_layout)
                    point_dialog_layout.addWidget(point_button_box)

                    point_button_box.rejected.connect(point_dialog.reject)
                    point_button_box.accepted.connect(point_dialog.accept)

                    if point_dialog.exec() == QDialog.DialogCode.Accepted: 
                        object_dict["Coords"].append(int(x.text()))
                        object_dict["Coords"].append(int(y.text()))
                        print(object_dict)
                        self.__controller.add_object(object_dict)

                case "Line":
                    line_dialog = QDialog(self)
                    line_dialog.setWindowTitle("Point Coordinates")
                    line_dialog_layout = QVBoxLayout(line_dialog)
                    line_dialog_form_layout = QFormLayout()
                    x1 = QLineEdit()
                    line_dialog_form_layout.addRow("X1:", x1)
                    y1 = QLineEdit()
                    line_dialog_form_layout.addRow("Y1:", y1)
                    x2 = QLineEdit()
                    line_dialog_form_layout.addRow("X2:", x2)
                    y2 = QLineEdit()
                    line_dialog_form_layout.addRow("Y2:", y2)
                    line_button_box = QDialogButtonBox(
                        QDialogButtonBox.StandardButton.Cancel |
                        QDialogButtonBox.StandardButton.Ok
                    )
                    line_dialog_layout.addLayout(line_dialog_form_layout)
                    line_dialog_layout.addWidget(line_button_box)


                    line_button_box.rejected.connect(line_dialog.reject)
                    line_button_box.accepted.connect(line_dialog.accept)

                    if line_dialog.exec() == QDialog.DialogCode.Accepted:
                        object_dict["Coords"].append(int(x1.text()))
                        object_dict["Coords"].append(int(y1.text()))
                        object_dict["Coords"].append(int(x2.text()))
                        object_dict["Coords"].append(int(y2.text()))
                        print(object_dict)
                        self.__controller.add_object(object_dict)

    def open_input_dialog(self):
        name, ok = QInputDialog.getText(
            self,
            'Name',
            'Name:'
        )

        if ok and name:
            self.setWindowTitle(name)

    def add_object_to_df(self, literal_object):
        self.display_file.append(literal_object)
        self.canvas.update()