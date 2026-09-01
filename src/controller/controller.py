from core.coordinate import Coordinate
from core.viewport import Viewport
from core.window import Window
from core.transformer import Transformer
from models.display_file import DisplayFile
from models.graphic_obj import GraphicObject
from models.line import Line
from models.obj_type import ObjectType
from models.point import Point
from models.wireframe import Wireframe
from view.interface import SGIInterface


_TYPE_MAP: dict[str, tuple[type[GraphicObject], ObjectType]] = {
    "Point": (Point, ObjectType.POINT),
    "Line": (Line, ObjectType.LINE),
    "Wireframe": (Wireframe, ObjectType.WIREFRAME),
}


class Controller:
    def __init__(self) -> None:
        self.display_file = DisplayFile()
        self.window = Window(0, 0, 600, 400)
        self.viewport = Viewport(0, 0, 600, 400)
        self.sgi = SGIInterface(self)
        self.transformer = Transformer(self.window)
        self.canvas = self.sgi.canvas

        self.testing()

    def add_object(self, obj_dict: dict) -> None:
        obj_class, obj_type = _TYPE_MAP[obj_dict["Type"]]
        self.display_file.add(obj_class, obj_type, obj_dict["Name"], obj_dict["Coords"])
        self.sgi.refresh_canvas()

    def remove_object(self, obj_id: int) -> None:
        self.display_file.remove(obj_id)
        self.sgi.refresh_canvas()

    def transform_object(self, transformation_dict: dict) -> None:
        object_id = int(transformation_dict["object"].split(" - ", 1)[0])
        match transformation_dict["operation"]:
            case("translation"):
                self.transformer.translate(self.display_file.get_by_id(object_id), transformation_dict["dx"], transformation_dict["dy"])
            case("rotation"):
                self.transformer.rotate(self.display_file.get_by_id(object_id), transformation_dict["angle"], transformation_dict["center"])
            case("scaling"):
                self.transformer.scale(self.display_file.get_by_id(object_id), transformation_dict["sx"], transformation_dict["sy"])
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_canvas()

    def pan(self, dx: float, dy: float) -> None:
        self.window.pan(dx, dy)
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_canvas()

    def zoom(self, factor: float) -> None:
        self.window.zoom(factor)
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_canvas()

    def rotate(self, factor: float) -> None:
        self.window.rotate(factor)
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_canvas()

    def resize_viewport(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            return

        self.viewport.resize(width, height)
        self.window.match_aspect_ratio(width / height)
        self.transformer.update_normalization_matrix(self.window)

    def get_drawable_objects(self) -> list[tuple[GraphicObject, list[Coordinate]]]:
        return [
            (obj, self.viewport.transform_all(self.transformer.normalize(obj), self.window)) for obj in self.display_file.objects
        ]

    def testing(self):
        self.add_object({"Name": "teste",
                         "Type": "Wireframe",
                         "Coords": [Coordinate(0,0), Coordinate(200, 200),
                                                     Coordinate(400,0)]})
