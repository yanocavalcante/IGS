import numpy as np
from .coordinate import Coordinate

class Transformer:
    def translate(self, obj, dx, dy):
        matrix = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        new_coords = []
        for coords in obj.coords:
            hom_new_coord = coords.homogeneous() @ matrix
            print(f"The results of the matrix multiplication is: {hom_new_coord}")
            new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))

        obj.coords = new_coords

        return

    def rotate(self, obj, angle):
        pass

    def scale(self, obj, sx, sy):
        pass