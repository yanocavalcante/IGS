from interface import SGIInterface
from point import Point
from line import Line
from obj_type import ObjectType

class Controller:
    def __init__(self) -> None:
        self.sgi = SGIInterface(self)

    def add_object(self, obj_dict):
        match obj_dict["Type"]:
            case "Point":
                self.sgi.add_object_to_df(Point(obj_dict["Name"], int(1), ObjectType.POINT, obj_dict["Coords"]))
            case "Line":
                self.sgi.add_object_to_df(Line(obj_dict["Name"], int(2), ObjectType.LINE, obj_dict["Coords"]))
            case "Polygon":
                pass

