from enum import Enum


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
    CURVE = 4
    BSPLINE = 5
    OBJECT_3D = 6
    BEZIER_SURFACE = 7
