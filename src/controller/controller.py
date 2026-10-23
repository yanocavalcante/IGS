from core.coordinate import Coordinate
from core.viewport import Viewport
from core.window import Window
from core.transformer import Transformer
from core.clipper import Clipper
from core.projection import Projection, ProjectionType
from models.display_file import DisplayFile
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType
from models.point import Point
from models.line import Line
from models.wireframe import Wireframe
from models.bezier_curve import BezierCurve
from models.bspline_curve import BSplineCurve
from models.object_3d import Object3D
from view.interface import SGIInterface


_TYPE_MAP: dict[str, tuple[type[GraphicObject], ObjectType]] = {
    "Point": (Point, ObjectType.POINT),
    "Line": (Line, ObjectType.LINE),
    "Wireframe": (Wireframe, ObjectType.WIREFRAME),
    "Curve": (BezierCurve, ObjectType.CURVE),
    "B-Spline": (BSplineCurve, ObjectType.BSPLINE),
    "3D Object": (Object3D, ObjectType.OBJECT_3D),
}


class Controller:
    def __init__(self) -> None:
        self.display_file = DisplayFile()
        self.__create_window()
        self.viewport = Viewport(0, 0, 600, 400)
        self.sgi = SGIInterface(self)
        self.transformer = Transformer(self.window)
        self.clipper = Clipper()
        self.canvas = self.sgi.canvas

        self.testing()

    def add_object(self, obj_dict: dict) -> None:
        obj_type_name = obj_dict["Type"]
        obj_class, obj_type = _TYPE_MAP[obj_type_name]
        self.display_file.add(obj_class, obj_type, obj_dict["Name"], obj_dict["Coords"],**({"edges": obj_dict["Edges"]} if "Edges" in obj_dict else {}))
        self.sgi.refresh_canvas()

    def remove_object(self, obj_id: int) -> None:
        self.display_file.remove(obj_id)
        self.sgi.refresh_canvas()

    def transform_object(self, transformation_dict: dict) -> None:
        object_id = int(transformation_dict["object"].split(" - ", 1)[0])
        obj = self.display_file.get_by_id(object_id)

        match transformation_dict["operation"]:
            case("translation"):
                self.transformer.translate(obj, transformation_dict["dx"], transformation_dict["dy"], transformation_dict.get("dz", 0.0))
            case("rotation"):
                self.transformer.rotate(obj, transformation_dict["angle"], transformation_dict["center"], transformation_dict.get("axis", "z"))
            case("scaling"):
                self.transformer.scale(obj, transformation_dict["sx"], transformation_dict["sy"], transformation_dict.get("sz", 1.0))
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_canvas()

    def pan(self, dx: float, dy: float, dz: float = 0.0) -> None:
        self.window.pan(dx, dy, dz)
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

    def rotate_view(self, axis: str, factor: float) -> None:
        self.window.rotate_view(axis, factor)
        self.sgi.refresh_canvas()

    def resize_viewport(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            return

        self.viewport.resize(width, height)
        self.window.match_aspect_ratio(width / height)
        self.transformer.update_normalization_matrix(self.window)
        self.sgi.refresh_projection_controls()

    def toggle_projection(self) -> None:
        self.window.toggle_projection()
        self.sgi.refresh_canvas()

    def move_cop(self, factor: float) -> None:
        self.window.move_cop(factor)
        self.sgi.refresh_canvas()

    def get_drawable_objects(self) -> list[tuple[GraphicObject, list[Coordinate]]]:
        drawable_objects = []

        for obj in self.display_file.objects:
            if not isinstance(obj, Object3D):
                continue

            obj.visible_edges = []
            for edge in self.__project_edges(obj):
                normalized_edge = self.transformer.normalize_coords(edge)
                clipped_edge = self.clipper.cohen_sutherland(normalized_edge)
                if clipped_edge:
                    obj.visible_edges.append(self.viewport.transform_all(clipped_edge, self.window))
            if obj.visible_edges:
                drawable_objects.append((obj, []))

        return drawable_objects

    def __project_edges(self, obj: Object3D) -> list[list[Coordinate]]:
        """Projects every edge of the object onto the projection plane (UV)."""
        if self.window.projection is ProjectionType.PERSPECTIVE:
            view = [Projection.view_space(coord, self.window) for coord in obj.coords]
            edges = (Projection.perspective_edge(view[start], view[end], self.window)
                     for start, end in obj.edges)

            return [edge for edge in edges if edge]

        projected = [Projection.parallel(coord, self.window) for coord in obj.coords]

        return [[projected[start], projected[end]] for start, end in obj.edges]

    def __clip_curve(self, coords: list[Coordinate]) -> list[list[Coordinate]]:
        """Clips a curve (polyline) segment by segment.

        Returns one polyline per visible stretch, so a curve leaving and
        re-entering the window is not joined by a spurious straight line.
        """
        runs: list[list[Coordinate]] = []

        for p1, p2 in zip(coords, coords[1:]):
            piece = self.clipper.cohen_sutherland([p1, p2])
            if not piece:
                continue

            if runs and runs[-1][-1] == piece[0]:
                runs[-1].append(piece[1])
            else:
                runs.append(list(piece))

        return runs

    def __create_window(self):
        self.window = Window([
            Coordinate(-300, -200, 0), Coordinate(-300, 200, 0),
            Coordinate(300, 200, 0), Coordinate(300, -200, 0),
        ])

    def testing(self):
        cube = [
            Coordinate(-180, -80, -60), Coordinate(-60, -80, -60),
            Coordinate(-60, 40, -60), Coordinate(-180, 40, -60),
            Coordinate(-180, -80, 60), Coordinate(-60, -80, 60),
            Coordinate(-60, 40, 60), Coordinate(-180, 40, 60),
        ]
        cube_edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                      (4, 5), (5, 6), (6, 7), (7, 4),
                      (0, 4), (1, 5), (2, 6), (3, 7)]
        self.add_object({"Name": "Cube", "Type": "3D Object", "Coords": cube, "Edges": cube_edges})

        pyramid = [
            Coordinate(60, -100, -60), Coordinate(180, -100, -60),
            Coordinate(180, 20, -60), Coordinate(60, 20, -60),
            Coordinate(120, -40, 100),
        ]
        pyramid_edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                         (0, 4), (1, 4), (2, 4), (3, 4)]
        self.add_object({"Name": "Pyramid", "Type": "3D Object", "Coords": pyramid, "Edges": pyramid_edges})
