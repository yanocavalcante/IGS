from core.coordinate import Coordinate
from core.viewport import Viewport
from core.window import Window
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
        self.canvas = self.sgi.canvas

        self.testing()

    def add_object(self, obj_dict: dict) -> None:
        obj_class, obj_type = _TYPE_MAP[obj_dict["Type"]]
        self.display_file.add(obj_class, obj_type, obj_dict["Name"], obj_dict["Coords"])
        self.sgi.refresh_canvas()

    def remove_object(self, obj_id: int) -> None:
        self.display_file.remove(obj_id)
        self.sgi.refresh_canvas()

    def pan(self, dx: float, dy: float) -> None:
        self.window.pan(dx, dy)
        self.sgi.refresh_canvas()

    def zoom(self, factor: float) -> None:
        self.window.zoom(factor)
        self.sgi.refresh_canvas()

    def resize_viewport(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            return

        self.viewport.resize(width, height)
        self.window.match_aspect_ratio(width / height)

    def get_drawable_objects(self) -> list[tuple[GraphicObject, list[Coordinate]]]:
        return [
            (obj, self.viewport.transform_all(obj.coords, self.window))
            for obj in self.display_file.objects
        ]

    def testing(self):
        self.add_object({"Name": "teste",
                         "Type": "Wireframe",
                         "Coords": [Coordinate(0,0), Coordinate(200, 200),
                                                     Coordinate(400,0)]})
