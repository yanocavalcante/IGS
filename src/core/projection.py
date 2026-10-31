from enum import Enum

import numpy as np
from core.coordinate import Coordinate


class ProjectionType(Enum):
    PARALLEL = 1
    PERSPECTIVE = 2


class Projection:
    """
    Projections from world space to the projection plane (UV coordinates).

    The camera is the one already defined by the Window: the rotations in
    `window.view_angles` align the VPN with the Z axis (steps 2 and 3 of the
    perspective algorithm), and the Window center is the VRP/CW, which lies
    on the projection plane.

    For perspective, the center of projection (COP) is virtual: it sits on
    the VPN line through the CW, `window.cop_distance` (d) behind the
    projection plane. Moving the COP closer (small d) gives a wide-angle look
    (strong convergence); moving it away (large d) gives a telephoto look,
    approaching the parallel projection as d grows.

    [IAGen] Perspective methods (view_space(), perspective_edge()) generated
    with the help of an LLM (see AIGen.md).
    """

    # Smallest depth (distance from the COP along the VPN) still projected.
    # Prevents division by zero / mirrored points for geometry at or behind
    # the COP. It is NOT a 3D clipping of the view volume: clipping on X and Y
    # is still done in 2D, after the projection.
    NEAR = 0.01

    @staticmethod
    def view_space(coord: Coordinate, window) -> np.ndarray:
        """Rotates the world so the VPN is aligned with Z. Returns (x, y, z)."""
        angle_x, angle_y, angle_z = np.deg2rad(window.view_angles)

        cosine_x, sine_x = np.cos(angle_x), np.sin(angle_x)
        cosine_y, sine_y = np.cos(angle_y), np.sin(angle_y)
        cosine_z, sine_z = np.cos(angle_z), np.sin(angle_z)

        rotation_x = np.array([[1, 0, 0], [0, cosine_x, sine_x], [0, -sine_x, cosine_x]])
        rotation_y = np.array([[cosine_y, 0, -sine_y], [0, 1, 0], [sine_y, 0, cosine_y]])
        rotation_z = np.array([[cosine_z, sine_z, 0], [-sine_z, cosine_z, 0], [0, 0, 1]])

        return np.array([coord.x, coord.y, coord.z]) @ rotation_x @ rotation_y @ rotation_z

    @staticmethod
    def parallel(coord: Coordinate, window) -> Coordinate:
        x, y, _ = Projection.view_space(coord, window)

        return Coordinate(float(x), float(y), 0.0)

    @staticmethod
    def perspective_edge(start: np.ndarray, end: np.ndarray, window) -> list[Coordinate]:
        """
        Projects an edge, given by its endpoints in view space, using the
        slides' special case (Eq. 6.2): with the COP translated to the origin
        and the projection plane at z = d, xp = x / (z / d) and yp = y / (z / d).

        The result is expressed in the plane's own UV coordinates (around the
        Window center), so the usual normalization applies. An edge entirely
        behind the COP yields []; an edge that crosses the COP depth is cut at
        Projection.NEAR before being projected.
        """
        center = window.center
        d = window.cop_distance

        # Viewing along -Z: depth grows from the COP towards the objects.
        depth_start = center.z + d - start[2]
        depth_end = center.z + d - end[2]

        if depth_start < Projection.NEAR and depth_end < Projection.NEAR:
            return []

        if depth_start < Projection.NEAR or depth_end < Projection.NEAR:
            t = (Projection.NEAR - depth_start) / (depth_end - depth_start)
            cut = start + t * (end - start)

            if depth_start < Projection.NEAR:
                start, depth_start = cut, Projection.NEAR
            else:
                end, depth_end = cut, Projection.NEAR

        return [
            Coordinate(float(center.x + (point[0] - center.x) * d / depth),
                       float(center.y + (point[1] - center.y) * d / depth),
                       0.0)
            for point, depth in ((start, depth_start), (end, depth_end))
        ]
