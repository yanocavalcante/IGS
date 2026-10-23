from .coordinate import Coordinate
from .projection import ProjectionType
import numpy as np


COP_MIN_DISTANCE = 20.0
COP_MAX_DISTANCE = 20000.0


class Window:
    def __init__(self, coords: list[Coordinate]) -> None:
        self.__coords = coords
        self.__theta_y = -30
        self.__theta_x = 25
        self.__theta_z = 0

        self.__projection = ProjectionType.PERSPECTIVE
        self.__cop_distance = 600.0

        self.__norm_xwmin = -1
        self.__norm_ywmin = -1
        self.__norm_xwmax = 1
        self.__norm_ywmax = 1

    @property
    def coords(self) -> list[Coordinate]:
        return self.__coords

    @property
    def xwmin(self) -> float:
        return self.__coords[0].x

    @property
    def ywmin(self) -> float:
        return self.__coords[0].y

    @property
    def zwmin(self) -> float:
        return self.__coords[0].z

    @property
    def xwmax(self) -> float:
        return self.__coords[2].x

    @property
    def ywmax(self) -> float:
        return self.__coords[2].y

    @property
    def zwmax(self) -> float:
        return self.__coords[2].z

    @property
    def norm_xwmin(self) -> float:
        return self.__norm_xwmin

    @property
    def norm_ywmin(self) -> float:
        return self.__norm_ywmin

    @property
    def norm_xwmax(self) -> float:
        return self.__norm_xwmax

    @property
    def norm_ywmax(self) -> float:
        return self.__norm_ywmax
      
    @property
    def width(self) -> float:
        return self.xwmax - self.xwmin

    @property
    def height(self) -> float:
        return self.ywmax - self.ywmin

    @property
    def center(self) -> Coordinate:
        return Coordinate((self.xwmin + self.xwmax)/2,
                                  (self.ywmin + self.ywmax)/2,
                                    (self.zwmin + self.zwmax)/2)

    @property
    def theta_x(self) -> float:
        return self.__theta_x

    @theta_x.setter
    def theta_x(self, value):
        self.__theta_x = value

    @property
    def theta_y(self) -> float:
        return self.__theta_y

    @theta_y.setter
    def theta_y(self, value):
        self.__theta_y = value

    @property
    def angle(self) -> float:
        return self.theta_y

    @property
    def view_angles(self) -> tuple[float, float, float]:
        return self.theta_x, self.theta_y, self.__theta_z

    @property
    def vup(self):
        theta_y = self.theta_y * (np.pi/180)

        return np.array([
            np.sin(theta_y),
             np.cos(theta_y)
        ])

    @property
    def vright(self):
        theta_y = self.theta_y * (np.pi/180)

        return np.array([
            np.cos(theta_y),
              -np.sin(theta_y)
        ])

    @property
    def projection(self) -> ProjectionType:
        return self.__projection

    @property
    def cop_distance(self) -> float:
        """Distance d from the (virtual) COP to the projection plane, along the VPN."""
        return self.__cop_distance

    @property
    def field_of_view(self) -> float:
        """Horizontal field of view, in degrees, subtended by the Window from the COP."""
        return float(np.degrees(2 * np.arctan((self.width / 2) / self.__cop_distance)))

    def toggle_projection(self) -> None:
        if self.__projection is ProjectionType.PERSPECTIVE:
            self.__projection = ProjectionType.PARALLEL
        else:
            self.__projection = ProjectionType.PERSPECTIVE

    def move_cop(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("COP factor must be greater than zero")

        self.__cop_distance = min(max(self.__cop_distance * factor, COP_MIN_DISTANCE), COP_MAX_DISTANCE)

    def pan(self, dx: float, dy: float, dz: float) -> None:
        for coord in self.__coords:
            coord.x += dx
            coord.y += dy
            coord.z += dz

    def zoom(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("Zoom factor must be greater than zero")

        center = self.center

        for coord in self.__coords:
            coord.x = center.x + (coord.x - center.x) * factor
            coord.y = center.y + (coord.y - center.y) * factor

    def rotate(self, angle: float) -> None:
        self.theta_y = (self.theta_y + angle) % 360

    def rotate_view(self, axis: str, angle: float) -> None:
        if axis == "x":
            self.theta_x = (self.theta_x + angle) % 360
        elif axis == "y":
            self.rotate(angle)
        elif axis == "z":
            self.__theta_z = (self.__theta_z + angle) % 360
        else:
            raise ValueError("View rotation axis must be x, y or z.")

    def match_aspect_ratio(self, aspect_ratio: float) -> None:
        if aspect_ratio <= 0:
            raise ValueError("Aspect ratio must be greater than zero")

        center = self.center

        half_height = self.height / 2
        half_width = half_height * aspect_ratio

        self.__coords[0].x = center.x - half_width
        self.__coords[1].x = center.x - half_width
        self.__coords[2].x = center.x + half_width
        self.__coords[3].x = center.x + half_width
