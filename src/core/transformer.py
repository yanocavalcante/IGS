import numpy as np
from .coordinate import Coordinate

class Transformer:
    def __init__(self, window):
        self.__normalization_matrix = self.update_normalization_matrix(window)

    @property
    def normalization_matrix(self):
        return self.__normalization_matrix

    @normalization_matrix.setter
    def normalization_matrix(self, value):
        self.__normalization_matrix = value

    def update_normalization_matrix(self, window):
        translation_norm_matrix = np.array([[1, 0, 0], [0, 1, 0], [-window.center.x, -window.center.y, 1]])
        scaling_norm_matrix = np.array([[2/window.width, 0, 0], [0, 2/window.height, 0], [0, 0, 1]])

        self.__normalization_matrix = translation_norm_matrix @ scaling_norm_matrix
        return self.__normalization_matrix

    def translate(self, obj, dx, dy, dz=0.0):
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                           [0, 0, 1, 0], [dx, dy, dz, 1]], dtype=float)
        
        self.__apply(obj, matrix)

    def rotate(self, obj, angle, center, axis="z"):
        angle = np.deg2rad(angle)
        cosine, sine = np.cos(angle), np.sin(angle)
        rotations = {
            "x": np.array([[1, 0, 0, 0], [0, cosine, sine, 0], [0, -sine, cosine, 0], [0, 0, 0, 1]]),
            "y": np.array([[cosine, 0, -sine, 0], [0, 1, 0, 0], [sine, 0, cosine, 0], [0, 0, 0, 1]]),
            "z": np.array([[cosine, sine, 0, 0], [-sine, cosine, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
        }

        if center == "world":
            pivot = (0.0, 0.0, 0.0)
        elif center == "object":
            pivot = self.__center_3d(obj)
        else:
            pivot = center

        to_origin = self.__translation_matrix(-pivot[0], -pivot[1], -pivot[2])
        from_origin = self.__translation_matrix(*pivot)
        self.__apply(obj, to_origin @ rotations[axis] @ from_origin)

    def scale(self, obj, sx, sy, sz=1.0):
        cx, cy, cz = self.__center_3d(obj)
        matrix = (self.__translation_matrix(-cx, -cy, -cz)
                  @ np.diag([sx, sy, sz, 1.0])
                  @ self.__translation_matrix(cx, cy, cz))
        self.__apply(obj, matrix)

    def normalize(self, obj):
        new_coords = self.normalize_coords(obj.coords)
        obj.norm_coords = new_coords
        return new_coords

    def normalize_coords(self, coords):
        return [self.__normalize_coordinate(coord) for coord in coords]

    def __normalize_coordinate(self, coord):
        hom_new_coord = np.array([coord.x, coord.y, 1.0]) @ self.__normalization_matrix
        return Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1]), coord.z)

    @staticmethod
    def __translation_matrix(dx, dy, dz):
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                         [0, 0, 1, 0], [dx, dy, dz, 1]], dtype=float)

    @staticmethod
    def __center_3d(obj):
        return tuple(sum(getattr(coord, axis) for coord in obj.coords) / len(obj.coords)
                     for axis in ("x", "y", "z"))

    @staticmethod
    def __apply(obj, matrix):
        obj.coords = [Coordinate(*(float(value) for value in (coord.homogeneous() @ matrix)[:3]))
                      for coord in obj.coords]
