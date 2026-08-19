from interface import SGIInterface
from point import Point
from obj_type import ObjectType

class Controller:
    def __init__(self) -> None:
        self.sgi = SGIInterface(self)

    def add_object(self, obj_dict):
        match obj_dict["Type"]:
            case "Point":
                self.sgi.add_object_to_df(Point(obj_dict["Name"], int(1), ObjectType.POINT, obj_dict["Coords"]))
            case "Line":
                pass
            case "Polygon":
                pass

