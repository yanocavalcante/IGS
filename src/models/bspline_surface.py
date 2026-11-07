import numpy as np

from core.coordinate import Coordinate
from models.graphic_obj import GraphicObject
from models.obj_type import ObjectType


class BSplineSurface(GraphicObject):
    """Uniform cubic B-spline surface rasterized with forward differences."""

    DEFAULT_STEPS = 10
    _BSPLINE_BASIS = np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 0, 3, 0],
        [1, 4, 1, 0],
    ], dtype=float) / 6.0

    def __init__(self, name: str, id: int, type: ObjectType,
                 coords: list[Coordinate], rows: int, cols: int) -> None:
        if not 4 <= rows <= 20 or not 4 <= cols <= 20:
            raise ValueError("A B-Spline surface must have from 4 to 20 rows and columns.")
        if len(coords) != rows * cols:
            raise ValueError("The control-point count does not match the supplied matrix dimensions.")

        super().__init__(name, id, type, coords)
        self.rows = rows
        self.cols = cols
        self.__visible_edges: list[list[Coordinate]] = []

    @property
    def patch_count(self) -> int:
        return (self.rows - 3) * (self.cols - 3)

    def _patch_matrices(self, row: int, col: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        patch = [[self.coords[(row + i) * self.cols + col + j] for j in range(4)] for i in range(4)]
        return tuple(np.array([[getattr(point, axis) for point in line] for line in patch], dtype=float)
                     for axis in ("x", "y", "z"))

    @staticmethod
    def _difference_matrix(delta: float) -> np.ndarray:
        delta2 = delta * delta
        delta3 = delta2 * delta
        return np.array([
            [0.0, 0.0, 0.0, 1.0],
            [delta3, delta2, delta, 0.0],
            [6.0 * delta3, 2.0 * delta2, 0.0, 0.0],
            [6.0 * delta3, 0.0, 0.0, 0.0],
        ])

    @staticmethod
    def _advance(differences: np.ndarray) -> None:
        """Advance one parameter step using only forward-difference sums."""
        differences[0] += differences[1]
        differences[1] += differences[2]
        differences[2] += differences[3]

    @classmethod
    def _curves_from_difference_grid(cls, grid: np.ndarray, steps: int) -> list[list[float]]:
        """Produces all isoparametric curves represented by a DD matrix."""
        state = grid.copy()
        curves: list[list[float]] = []
        for _ in range(steps + 1):
            value, first, second, third = state[0]
            curve = [float(value)]
            for _ in range(steps):
                value += first
                first += second
                second += third
                curve.append(float(value))
            curves.append(curve)
            cls._advance(state)
        return curves

    def wireframe_edges(self, steps: int = DEFAULT_STEPS) -> list[tuple[Coordinate, Coordinate]]:
        if steps < 1:
            raise ValueError("Surface tessellation needs at least one step.")

        delta = 1.0 / steps
        e = self._difference_matrix(delta)
        edges: list[tuple[Coordinate, Coordinate]] = []

        for patch_row in range(self.rows - 3):
            for patch_col in range(self.cols - 3):
                matrices = self._patch_matrices(patch_row, patch_col)
                # DD = E(delta_u) . M . G . M^T . E(delta_v)^T.
                # It contains the initial forward differences in both parameters.
                dd = [e @ self._BSPLINE_BASIS @ matrix @ self._BSPLINE_BASIS.T @ e.T
                      for matrix in matrices]

                u_curves = [self._curves_from_difference_grid(matrix, steps) for matrix in dd]
                v_curves = [self._curves_from_difference_grid(matrix.T, steps) for matrix in dd]
                for curves in (u_curves, v_curves):
                    for line in range(steps + 1):
                        for point in range(steps):
                            edges.append((
                                Coordinate(curves[0][line][point], curves[1][line][point], curves[2][line][point]),
                                Coordinate(curves[0][line][point + 1], curves[1][line][point + 1], curves[2][line][point + 1]),
                            ))
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
