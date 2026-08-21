from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from view.canvas import Canvas
from view.dialogs.create_object_dialog import CreateObjectDialog

PAN_STEP = 20        
ZOOM_IN_FACTOR = 0.9  
ZOOM_OUT_FACTOR = 1.1


class SGIInterface(QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.__controller = controller
        self.setWindowTitle("Interactive Graphic System")
        self.setGeometry(100, 100, 1024, 768)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.__create_menu()
        self.__create_canvas()

    def __create_canvas(self) -> None:
        self.canvas = Canvas(self.__controller)
        self.main_layout.addWidget(self.canvas, 4)

    def __create_menu(self) -> None:
        menu = QWidget()
        menu_layout = QVBoxLayout(menu)
        self.main_layout.addWidget(menu, 1)

        menu_layout.addWidget(QLabel("Zoom"))
        zoom_layout = QGridLayout()
        self.__add_button(zoom_layout, "Zoom +", self.__zoom_in, 0, 0)
        self.__add_button(zoom_layout, "Zoom -", self.__zoom_out, 0, 1)
        menu_layout.addLayout(zoom_layout)

        menu_layout.addWidget(QLabel("Navigation"))
        nav_layout = QGridLayout()
        self.__add_button(nav_layout, "Up", self.__move_up, 1, 1)
        self.__add_button(nav_layout, "Left", self.__move_left, 2, 0)
        self.__add_button(nav_layout, "Down", self.__move_down, 2, 1)
        self.__add_button(nav_layout, "Right", self.__move_right, 2, 2)
        menu_layout.addLayout(nav_layout)

        menu_layout.addWidget(QLabel("Objects"))
        objects_layout = QGridLayout()
        self.__add_button(objects_layout, "Create New Object", self.__create_object, 0, 0)
        menu_layout.addLayout(objects_layout)

        menu_layout.addWidget(QLabel("Display File"))
        self.object_list = QListWidget()
        menu_layout.addWidget(self.object_list)

        menu_layout.addStretch()

    def __add_button(self, layout, text, callback, row, column) -> None:
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button, row, column)

    def __zoom_in(self) -> None:
        self.__controller.zoom(ZOOM_IN_FACTOR)

    def __zoom_out(self) -> None:
        self.__controller.zoom(ZOOM_OUT_FACTOR)

    def __move_up(self) -> None:
        self.__controller.pan(0, PAN_STEP)

    def __move_down(self) -> None:
        self.__controller.pan(0, -PAN_STEP)

    def __move_left(self) -> None:
        self.__controller.pan(-PAN_STEP, 0)

    def __move_right(self) -> None:
        self.__controller.pan(PAN_STEP, 0)

    def __create_object(self) -> None:
        dialog = CreateObjectDialog(self)
        obj_dict = dialog.get_object_dict()
        if obj_dict is not None:
            self.__controller.add_object(obj_dict)

    def refresh_canvas(self) -> None:
        self.canvas.update()
        self.__refresh_object_list()

    def __refresh_object_list(self) -> None:
        self.object_list.clear()
        for obj in self.__controller.display_file.objects:
            self.object_list.addItem(f"{obj.type.name}({obj.name})")


__all__ = ["SGIInterface", "QApplication"]
