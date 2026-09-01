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

    def rotate(self, obj, angle, center):
        # Should/Could we use the function 'translate' to do parts of it?
        cx, cy = obj.center()
        # Numpy uses radians instead of degrees
        angle = angle * (np.pi/180)

        origin_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [-cx, -cy, 1]])
        rotate_matrix = np.array([[np.cos(angle), np.sin(angle), 0],
                           [-np.sin(angle), np.cos(angle), 0],
                           [0, 0 , 1]])
        center_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])
        new_coords = []

        match center:
            case("world"):
                for coords in obj.coords:
                    hom_new_coord = coords.homogeneous() @ rotate_matrix
                    new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))
            case("object"):
                for coords in obj.coords:
                    hom_new_coord = coords.homogeneous() @ origin_trans_matrix @ rotate_matrix @ center_trans_matrix
                    new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))             
            case _:
                minus_arbitrary_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [-center[0], -center[1], 1]])
                arbitrary_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [center[0], center[1], 1]])
                for coords in obj.coords:
                    hom_new_coord = coords.homogeneous() @ minus_arbitrary_trans_matrix @ rotate_matrix @ arbitrary_trans_matrix
                    new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))

        obj.coords = new_coords

        return

    def scale(self, obj, sx, sy):
        # Should/Could we use the function 'translate' to do parts of it?
        cx, cy = obj.center()

        origin_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [-cx, -cy, 1]])
        scale_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        center_trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [cx, cy, 1]])

        new_coords = []
        for coords in obj.coords:
            hom_new_coord = coords.homogeneous() @ origin_trans_matrix @ scale_matrix @ center_trans_matrix
            new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))

        obj.coords = new_coords

        return

    def normalize(self, obj, window):
        angle = window.angle * (np.pi/180)
        translation_norm_matrix = np.array([[1, 0, 0], [0, 1, 0], [-window.center[0], -window.center[1], 1]])
        rotation_norm_matrix = np.array([[np.cos(angle), np.sin(angle), 0], 
                                         [-np.sin(angle), np.cos(angle), 0], 
                                         [0, 0, 1]])
        scaling_norm_matrix = np.array([[1/3, 0, 0], [0, 1/2, 0], [0, 0, 1]])

        normalization_matrix = translation_norm_matrix @ rotation_norm_matrix @ scaling_norm_matrix

        new_coords = []
        for coords in obj.coords:
            hom_new_coord = coords.homogeneous() @ normalization_matrix
            new_coords.append(Coordinate(float(hom_new_coord[0]), float(hom_new_coord[1])))

        obj.norm_coords = new_coords

        return