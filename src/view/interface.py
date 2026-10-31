from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox
)

from core.projection import ProjectionType
from view.canvas import Canvas
from view.dialogs.create_object_dialog import CreateObjectDialog
from view.dialogs.transform_object_dialog import TransformObjectDialog

PAN_STEP = 20        
ZOOM_IN_FACTOR = 0.9  
ZOOM_OUT_FACTOR = 1.1
ROTATION_FACTOR = 15
COP_CLOSER_FACTOR = 0.8
COP_FARTHER_FACTOR = 1.25


class SGIInterface(QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.__controller = controller
        self.__pending_transformation: dict | None = None
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
        self.main_layout.addWidget(self.canvas, 3)

    def __create_menu(self) -> None:
        self.menu = QWidget()
        menu_layout = QVBoxLayout(self.menu)
        self.main_layout.addWidget(self.menu, 1)

        menu_layout.addWidget(QLabel("Zoom"))
        zoom_layout = QGridLayout()
        self.__add_button(zoom_layout, "Zoom +", self.__zoom_in, 0, 0)
        self.__add_button(zoom_layout, "Zoom -", self.__zoom_out, 0, 1)
        menu_layout.addLayout(zoom_layout)

        menu_layout.addWidget(QLabel("Navigation"))
        nav_layout = QGridLayout()
        self.__add_button(nav_layout, "Yaw Left", self.__rotate_left, 1, 0)
        self.__add_button(nav_layout, "Up", self.__move_up, 1, 1)
        self.__add_button(nav_layout, "Yaw Right", self.__rotate_right, 1, 2)
        self.__add_button(nav_layout, "Left", self.__move_left, 2, 0)
        self.__add_button(nav_layout, "Down", self.__move_down, 2, 1)
        self.__add_button(nav_layout, "Right", self.__move_right, 2, 2)
        self.__add_button(nav_layout, "Pitch +", self.__pitch_up, 3, 0)
        self.__add_button(nav_layout, "Pitch -", self.__pitch_down, 3, 2)
        
        self.angle_label = QLabel("Yaw: -30°")
        nav_layout.addWidget(self.angle_label)

        menu_layout.addLayout(nav_layout)

        menu_layout.addWidget(QLabel("Projection"))
        projection_layout = QGridLayout()
        self.projection_button = QPushButton()
        self.projection_button.clicked.connect(self.__toggle_projection)
        projection_layout.addWidget(self.projection_button, 0, 0, 1, 2)
        self.cop_closer_button = self.__add_button(projection_layout, "COP - (wide)", self.__cop_closer, 1, 0)
        self.cop_farther_button = self.__add_button(projection_layout, "COP + (tele)", self.__cop_farther, 1, 1)
        self.cop_label = QLabel()
        projection_layout.addWidget(self.cop_label, 2, 0, 1, 2)
        menu_layout.addLayout(projection_layout)

        menu_layout.addWidget(QLabel("Objects"))
        objects_layout = QGridLayout()
        self.__add_button(objects_layout, "Create", self.__create_object, 0, 0)
        self.__add_button(objects_layout, "Transform", self.__transform, 0, 1)
        self.__add_button(objects_layout, "Load .obj", self.__load_obj, 1, 0)
        self.__add_button(objects_layout, "Load surface .obj", self.__load_bezier_surface, 1, 1)

        menu_layout.addLayout(objects_layout)

        menu_layout.addWidget(QLabel("Display File"))
        self.object_list = QListWidget()
        menu_layout.addWidget(self.object_list)

        menu_layout.addStretch()

    def __add_button(self, layout, text, callback, row, column, column_span=1) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button, row, column, 1, column_span)

        return button

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

    def __rotate_left(self) -> None:
        self.__controller.rotate(+ROTATION_FACTOR)
        self.angle_label.setText(
            f"Yaw: {self.__controller.window.angle:.0f}°"
        )

    def __rotate_right(self) -> None:
        self.__controller.rotate(-ROTATION_FACTOR)
        self.angle_label.setText(
            f"Yaw: {self.__controller.window.angle:.0f}°"
        )

    def __pitch_up(self) -> None:
        self.__controller.rotate_view("x", ROTATION_FACTOR)

    def __pitch_down(self) -> None:
        self.__controller.rotate_view("x", -ROTATION_FACTOR)

    def __toggle_projection(self) -> None:
        self.__controller.toggle_projection()

    def __cop_closer(self) -> None:
        self.__controller.move_cop(COP_CLOSER_FACTOR)

    def __cop_farther(self) -> None:
        self.__controller.move_cop(COP_FARTHER_FACTOR)

    def refresh_projection_controls(self) -> None:
        """[IAGen] Generated with the help of an LLM (see AIGen.md)."""
        window = self.__controller.window
        perspective = window.projection is ProjectionType.PERSPECTIVE

        self.projection_button.setText("Projection: Perspective" if perspective else "Projection: Parallel")
        self.cop_closer_button.setEnabled(perspective)
        self.cop_farther_button.setEnabled(perspective)

        if not perspective:
            self.cop_label.setText("COP at infinity")
            return

        fov = window.field_of_view
        kind = "wide-angle" if fov >= 70 else "telephoto" if fov <= 30 else "normal"
        self.cop_label.setText(f"COP d = {window.cop_distance:.0f} | FOV {fov:.0f}° ({kind})")

    def __create_object(self) -> None:
        dialog = CreateObjectDialog(self)
        obj_dict = dialog.get_object_dict()
        if obj_dict is not None:
            self.__controller.add_object(obj_dict)

    def __load_obj(self) -> None:
        """[IAGen] Generated with the help of an LLM (see AIGen.md)."""
        models_dir = Path(__file__).resolve().parents[2] / "assets" / "models"
        path, _ = QFileDialog.getOpenFileName(
            self, "Load wireframe model", str(models_dir) if models_dir.is_dir() else "",
            "Wavefront OBJ (*.obj)")
        if not path:
            return

        try:
            self.__controller.load_obj(path, Path(path).stem)
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "IGS", f"Could not load '{Path(path).name}':\n{error}")

    def __load_bezier_surface(self) -> None:
        models_dir = Path(__file__).resolve().parents[2] / "assets" / "models"
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Bézier surface control meshes", str(models_dir) if models_dir.is_dir() else "",
            "Wavefront OBJ (*.obj)")
        if not path:
            return

        try:
            self.__controller.load_bezier_surface(path, Path(path).stem)
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "IGS", f"Could not load '{Path(path).name}':\n{error}")

    def __transform(self) -> None:
        current_obj = self.object_list.currentItem()
        if not current_obj:
            QMessageBox.warning(self, "IGS", "Please select an object to transform!")
            return

        dialog = TransformObjectDialog(current_obj.text(), self)
        transformation_dict = dialog.get_object_transformation_dict()
        if transformation_dict is not None:
            self.__controller.transform_object(transformation_dict)

    def refresh_canvas(self) -> None:
        self.canvas.update()
        self.__refresh_object_list()
        self.refresh_projection_controls()

    def __refresh_object_list(self) -> None:
        self.object_list.clear()
        for obj in self.__controller.display_file.objects:
            self.object_list.addItem(f"{obj.id} - '{obj.name}'({obj.type.name})")


__all__ = ["SGIInterface", "QApplication"]
