import numpy as np

from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class BezierSurface(GraphicObject):
    DEFAULT_STEPS = 10
    _BEZIER_BASIS = np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0],
    ], dtype=float)

    def __init__(self, name: str, id: int, type: ObjectType,
                 coords: list[Coordinate]) -> None:
        if not coords or len(coords) % 16 != 0:
            raise ValueError("A Bézier surface needs one or more 4x4 patches (16 control points each).")
        super().__init__(name, id, type, coords)
        self.__visible_edges: list[list[Coordinate]] = []

    @property
    def patches(self) -> list[list[list[Coordinate]]]:
        return [
            [self.coords[offset + row * 4: offset + (row + 1) * 4] for row in range(4)]
            for offset in range(0, len(self.coords), 16)
        ]

    @property
    def patch_count(self) -> int:
        return len(self.coords) // 16

    @property
    def geometry_matrices(self) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """Returns the Gx, Gy and Gz 4x4 geometry matrices for each patch."""
        return [tuple(np.array(
            [[getattr(point, axis) for point in row] for row in patch], dtype=float
        ) for axis in ("x", "y", "z")) for patch in self.patches]

    def wireframe_edges(self, steps: int = DEFAULT_STEPS) -> list[tuple[Coordinate, Coordinate]]:
        if steps < 1:
            raise ValueError("Surface tessellation needs at least one step.")

        parameters = np.linspace(0.0, 1.0, steps + 1)
        basis = np.array([[u ** 3, u ** 2, u, 1.0] @ self._BEZIER_BASIS
                          for u in parameters])
        edges: list[tuple[Coordinate, Coordinate]] = []

        for matrices in self.geometry_matrices:
            grid = [[Coordinate(
                float(basis[i] @ matrices[0] @ basis[j]),
                float(basis[i] @ matrices[1] @ basis[j]),
                float(basis[i] @ matrices[2] @ basis[j]),
            ) for j in range(steps + 1)] for i in range(steps + 1)]

            for i in range(steps + 1):
                for j in range(steps):
                    edges.append((grid[i][j], grid[i][j + 1]))
                    edges.append((grid[j][i], grid[j + 1][i]))

        return edges

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        for p1, p2 in self.visible_edges:
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))

    @property
    def visible_edges(self) -> list[list[Coordinate]]:
        return self.__visible_edges

    @visible_edges.setter
    def visible_edges(self, value: list[list[Coordinate]]) -> None:
        self.__visible_edges = value
