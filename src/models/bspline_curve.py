from core.coordinate import Coordinate
from models.obj_type import ObjectType
from .graphic_obj import GraphicObject
import numpy as np


class BSplineCurve(GraphicObject):
    """
    Curva B-Spline cúbica uniforme rasterizada por Forward Differences.

    Uma B-Spline com n pontos de controle (n >= 4) é formada por n - 3
    segmentos cúbicos. Cada segmento é definido por 4 pontos de controle
    consecutivos e, em vez de recalcular as blending functions a cada passo
    de t, os coeficientes polinomiais (C = M_BS . G) são convertidos em
    diferenças finitas iniciais (E(delta) . C) e a curva é percorrida
    incrementalmente com apenas somas (ver DesenhaCurvaFwdDiff nos slides).

    [IAGen] Implementação desta classe e de seus métodos gerada com auxílio
    de LLM (ver AIGen.md).
    """

    _DELTA = 0.01

    def __init__(self, name: str, id: int, type: ObjectType, coords: list[Coordinate]) -> None:
        super().__init__(name, id, type, coords)
        self.__control_coords = coords
        self.forward_differences()

    @property
    def control_coords(self) -> list[Coordinate]:
        return self.__control_coords

    def draw(self, painter, vp_coords: list[Coordinate]) -> None:
        n = len(vp_coords)

        if n < 2:
            return

        for i in range(n - 1):
            p1, p2 = vp_coords[i], vp_coords[i + 1]
            painter.drawLine(round(p1.x), round(p1.y), round(p2.x), round(p2.y))

    def forward_differences(self) -> None:
        m_bs = np.array([
            [-1,  3, -3, 1],
            [ 3, -6,  3, 0],
            [-3,  0,  3, 0],
            [ 1,  4,  1, 0]
        ], dtype=float) / 6.0

        delta = self._DELTA
        delta2 = delta * delta
        delta3 = delta2 * delta

        e = np.array([
            [0,           0,           0,         1],
            [delta3,      delta2,      delta,     0],
            [6 * delta3,  2 * delta2,  0,         0],
            [6 * delta3,  0,           0,         0]
        ], dtype=float)

        steps = int(round(1 / delta))

        control = self.__control_coords
        curve: list[Coordinate] = []

        for i in range(len(control) - 3):
            gx = np.array([[control[i + k].x] for k in range(4)], dtype=float)
            gy = np.array([[control[i + k].y] for k in range(4)], dtype=float)

            fx = e @ (m_bs @ gx)
            fy = e @ (m_bs @ gy)

            segment = self.__fwd_diff(steps, fx, fy)

            if curve:
                segment = segment[1:]

            curve.extend(segment)

        self.coords = curve

    @staticmethod
    def __fwd_diff(steps: int, fx: np.ndarray, fy: np.ndarray) -> list[Coordinate]:
        """
        Percorre incrementalmente um segmento cúbico com forward differences.

        fx e fy são as colunas [f, delta(f), delta^2(f), delta^3(f)] iniciais
        calculadas para cada coordenada. A cada passo apenas somas são
        realizadas: x += dx; dx += d2x; d2x += d3x (análogo para y).

        [IAGen] Trecho gerado com auxílio de LLM (ver AIGen.md).
        """
        x, dx, d2x, d3x = fx[0, 0], fx[1, 0], fx[2, 0], fx[3, 0]
        y, dy, d2y, d3y = fy[0, 0], fy[1, 0], fy[2, 0], fy[3, 0]

        points = [Coordinate(x, y)]

        for _ in range(steps):
            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y

            points.append(Coordinate(x, y))

        return points