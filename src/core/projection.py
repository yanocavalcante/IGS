import numpy as np
from core.coordinate import Coordinate


class Projection:
    @staticmethod
    def parallel(coord: Coordinate, window) -> Coordinate:
        angle_x, angle_y, angle_z = np.deg2rad(window.view_angles)

        cosine_x, sine_x = np.cos(angle_x), np.sin(angle_x)
        cosine_y, sine_y = np.cos(angle_y), np.sin(angle_y)
        cosine_z, sine_z = np.cos(angle_z), np.sin(angle_z)

        rotation_x = np.array([[1, 0, 0], [0, cosine_x, sine_x], [0, -sine_x, cosine_x]])
        rotation_y = np.array([[cosine_y, 0, -sine_y], [0, 1, 0], [sine_y, 0, cosine_y]])
        rotation_z = np.array([[cosine_z, sine_z, 0], [-sine_z, cosine_z, 0], [0, 0, 1]])

        x, y, _ = np.array([coord.x, coord.y, coord.z]) @ rotation_x @ rotation_y @ rotation_z

        return Coordinate(float(x), float(y), 0.0)
