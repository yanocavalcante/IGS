from core.coordinate import Coordinate


class Clipper:
    def __init__(self) -> None:
        self.__clip = [
            Coordinate(-1, -1),
            Coordinate(1, -1),
            Coordinate(1, 1),
            Coordinate(-1, 1)
        ]
    def clipping(self, coords) -> list[list[Coordinate]]:
        match len(coords):
            case(1):
                return [coords]
            case(2):
                return [self.cohen_sutherland(coords)]
            case _:
                return self.weiler_atherton(coords)

    def cohen_sutherland(self, coords) -> list[Coordinate]:
        p1, p2 = coords

        rc1 = self.__calculate_rc(p1)
        rc2 = self.__calculate_rc(p2)

        while True:
            if (rc1 | rc2) == 0b0000:
                return [p1, p2]

            if (rc1 & rc2) != 0b0000:
                return [Coordinate(0, 0), Coordinate(0, 0)]

            if rc1 != 0b0000:
                rc = rc1
                p = p1
            else:
                rc = rc2
                p = p2

            if rc & 0b0001:
                y = (p2.y - p1.y) * (-1 - p.x) / (p2.x - p1.x) + p.y
                x = -1

            elif rc & 0b0010:
                y = (p2.y - p1.y) * (1 - p.x) / (p2.x - p1.x) + p.y
                x = 1

            elif rc & 0b1000:
                x = p.x + (p2.x - p1.x) * (1 - p.y) / (p2.y - p1.y)
                y = 1

            elif rc & 0b0100:
                x = p.x + (p2.x - p1.x) * (-1 - p.y) / (p2.y - p1.y)
                y = -1

            intersection = Coordinate(x, y)

            if rc == rc1:
                p1 = intersection
                rc1 = self.__calculate_rc(p1)
            else:
                p2 = intersection
                rc2 = self.__calculate_rc(p2)

    def liang_barsky(self, line):
        pass

    def nicholl_lee_nicholl(self, line):
        pass

    def weiler_atherton(self, coords: list[Coordinate]) -> list[list[Coordinate]]:
        obj = list(coords)
        clip = self.__clip

        n_obj = len(obj)
        n_clip = len(clip)

        if n_obj < 3:
            return []

        # ---------------------------------------------------------
        # 1. Encontrar todas as interseções entre OBJ e CLIP
        # ---------------------------------------------------------

        intersections = []

        for i in range(n_obj):
            p1 = obj[i]
            p2 = obj[(i + 1) % n_obj]

            edge_intersections = self.__find_intersections(p1, p2)

            for point, t_obj, clip_edge, t_clip in edge_intersections:
                intersections.append({
                    "point": point,
                    "obj_edge": i,
                    "t_obj": t_obj,
                    "clip_edge": clip_edge,
                    "t_clip": t_clip,
                    "entry": None,
                    "visited": False,
                    "obj_node": None,
                    "clip_node": None
                })

        # ---------------------------------------------------------
        # 2. Função para verificar se um ponto está dentro da Window
        # ---------------------------------------------------------

        def inside_window(point: Coordinate) -> bool:
            return (
                -1 <= point.x <= 1 and
                -1 <= point.y <= 1
            )

        # ---------------------------------------------------------
        # 3. Classificar as interseções como entrada ou saída
        # ---------------------------------------------------------

        epsilon = 1e-7

        for intersection in intersections:
            edge = intersection["obj_edge"]
            t = intersection["t_obj"]

            p1 = obj[edge]
            p2 = obj[(edge + 1) % n_obj]

            t_before = max(0.0, t - epsilon)
            t_after = min(1.0, t + epsilon)

            before = Coordinate(
                p1.x + t_before * (p2.x - p1.x),
                p1.y + t_before * (p2.y - p1.y)
            )

            after = Coordinate(
                p1.x + t_after * (p2.x - p1.x),
                p1.y + t_after * (p2.y - p1.y)
            )

            inside_before = inside_window(before)
            inside_after = inside_window(after)

            if not inside_before and inside_after:
                intersection["entry"] = True

            elif inside_before and not inside_after:
                intersection["entry"] = False

        # ---------------------------------------------------------
        # 4. Organizar as interseções por aresta
        # ---------------------------------------------------------

        obj_intersections = [[] for _ in range(n_obj)]
        clip_intersections = [[] for _ in range(n_clip)]

        for intersection in intersections:
            obj_intersections[intersection["obj_edge"]].append(intersection)
            clip_intersections[intersection["clip_edge"]].append(intersection)

        for edge_intersections in obj_intersections:
            edge_intersections.sort(key=lambda x: x["t_obj"])

        for edge_intersections in clip_intersections:
            edge_intersections.sort(key=lambda x: x["t_clip"])

        # ---------------------------------------------------------
        # 5. Construir a lista OBJ com as interseções inseridas
        # ---------------------------------------------------------

        obj_nodes = []

        for i in range(n_obj):
            obj_nodes.append({
                "coord": obj[i],
                "intersection": False,
                "entry": None,
                "event": None,
                "neighbor": None
            })

            for intersection in obj_intersections[i]:
                node = {
                    "coord": intersection["point"],
                    "intersection": True,
                    "entry": intersection["entry"],
                    "event": intersection,
                    "neighbor": None
                }

                intersection["obj_node"] = node
                obj_nodes.append(node)

        # ---------------------------------------------------------
        # 6. Construir a lista CLIP com as interseções inseridas
        # ---------------------------------------------------------

        clip_nodes = []

        for i in range(n_clip):
            clip_nodes.append({
                "coord": clip[i],
                "intersection": False,
                "entry": None,
                "event": None,
                "neighbor": None
            })

            for intersection in clip_intersections[i]:
                node = {
                    "coord": intersection["point"],
                    "intersection": True,
                    "entry": intersection["entry"],
                    "event": intersection,
                    "neighbor": None
                }

                intersection["clip_node"] = node
                clip_nodes.append(node)

        # ---------------------------------------------------------
        # 7. Conectar as interseções correspondentes
        # ---------------------------------------------------------

        for intersection in intersections:
            obj_node = intersection["obj_node"]
            clip_node = intersection["clip_node"]

            obj_node["neighbor"] = clip_node
            clip_node["neighbor"] = obj_node

        # ---------------------------------------------------------
        # 8. Casos sem interseção
        # ---------------------------------------------------------

        if not intersections:
            if all(inside_window(point) for point in obj):
                return [obj]

            if any(self.__point_inside_polygon(point, obj) for point in clip):
                return [clip]

            return []

        # ---------------------------------------------------------
        # 9. Determinar a direção de percurso da CLIP
        # ---------------------------------------------------------

        def polygon_area(points: list[Coordinate]) -> float:
            area = 0.0

            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]

                area += p1.x * p2.y - p2.x * p1.y

            return area / 2.0

        obj_ccw = polygon_area(obj) > 0
        clip_ccw = polygon_area(clip) > 0

        if clip_ccw == obj_ccw:
            clip_step = 1
        else:
            clip_step = -1

        # ---------------------------------------------------------
        # 10. Índices para percorrer circularmente as listas
        # ---------------------------------------------------------

        obj_index = {
            id(node): i
            for i, node in enumerate(obj_nodes)
        }

        clip_index = {
            id(node): i
            for i, node in enumerate(clip_nodes)
        }

        # ---------------------------------------------------------
        # 11. Reconstruir os polígonos resultantes
        # ---------------------------------------------------------

        result = []

        for start in obj_nodes:

            if not start["intersection"]:
                continue

            if not start["entry"]:
                continue

            if start["event"]["visited"]:
                continue

            polygon = []

            current = start
            mode = "obj"

            start["event"]["visited"] = True

            polygon.append(start["coord"])

            while True:

                # ---------------------------------------------
                # Percorrendo OBJ
                # ---------------------------------------------

                if mode == "obj":
                    index = obj_index[id(current)]
                    next_index = (index + 1) % len(obj_nodes)

                    current = obj_nodes[next_index]

                    if current is start:
                        break

                    polygon.append(current["coord"])

                    if current["intersection"]:
                        current["event"]["visited"] = True

                        # Saída: trocar OBJ por CLIP
                        if not current["entry"]:
                            current = current["neighbor"]
                            mode = "clip"

                # ---------------------------------------------
                # Percorrendo CLIP
                # ---------------------------------------------

                else:
                    index = clip_index[id(current)]
                    next_index = (index + clip_step) % len(clip_nodes)

                    current = clip_nodes[next_index]

                    if current is start:
                        break

                    polygon.append(current["coord"])

                    if current["intersection"]:
                        current["event"]["visited"] = True

                        # Entrada: voltar para OBJ
                        if current["entry"]:
                            current = current["neighbor"]
                            mode = "obj"

                            if current is start:
                                break

            if len(polygon) >= 3:
                result.append(self.__remove_repeated_points(polygon))

        if not result and any(self.__point_inside_polygon(point, obj) for point in clip):
            return [clip]

        return result

    def __point_inside_polygon(self, point: Coordinate, polygon: list[Coordinate]) -> bool:
        inside = False
        n = len(polygon)

        for i in range(n):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % n]

            if self.__point_on_segment(point, p1, p2):
                return True

            crosses_y = (p1.y > point.y) != (p2.y > point.y)

            if not crosses_y:
                continue

            x_intersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x

            if point.x < x_intersection:
                inside = not inside

        return inside

    def __point_on_segment(self, point: Coordinate, p1: Coordinate,
                           p2: Coordinate, epsilon: float = 1e-7) -> bool:
        cross = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)

        if abs(cross) > epsilon:
            return False

        return (
            min(p1.x, p2.x) - epsilon <= point.x <= max(p1.x, p2.x) + epsilon and
            min(p1.y, p2.y) - epsilon <= point.y <= max(p1.y, p2.y) + epsilon
        )

    def __remove_repeated_points(self, points: list[Coordinate],
                                 epsilon: float = 1e-7) -> list[Coordinate]:
        clean_points = []

        for point in points:
            if clean_points and self.__same_point(clean_points[-1], point, epsilon):
                continue

            clean_points.append(point)

        if len(clean_points) > 1 and self.__same_point(clean_points[0], clean_points[-1], epsilon):
            clean_points.pop()

        return clean_points

    def __same_point(self, p1: Coordinate, p2: Coordinate,
                     epsilon: float = 1e-7) -> bool:
        return abs(p1.x - p2.x) <= epsilon and abs(p1.y - p2.y) <= epsilon

    def __calculate_intersection(self, p1, p2, w1, w2):
        '''
        Calculates the intersection point between the edge of two OBJ points
        and two Window points 
        '''
        dx1 = p2.x - p1.x
        dy1 = p2.y - p1.y

        dx2 = w2.x - w1.x
        dy2 = w2.y - w1.y

        denominator = dx1 * dy2 - dy1 * dx2

        if denominator == 0:
            return None

        dx = w1.x - p1.x
        dy = w1.y - p1.y

        t = (dx * dy2 - dy * dx2) / denominator
        u = (dx * dy1 - dy * dx1) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            return Coordinate(p1.x + t * dx1, p1.y + t * dy1), t, u
        
        return None

    def __find_intersections(self, p1, p2):
        '''
        Given two points of a OBJ, find all of its intersections with the
        Window (clipper object, in this cenario)
        '''

        intersections = []
        for i in range(4):
            w1 = self.__clip[i]
            w2 = self.__clip[(i + 1) % 4]

            result = self.__calculate_intersection(p1, p2, w1, w2)

            if result is None:
                continue

            point, t_obj, t_clip = result

            if any(self.__same_point(point, existing[0]) for existing in intersections):
                continue

            intersections.append((point, t_obj, i, t_clip))

        intersections.sort(key=lambda intersection: intersection[1])

        return intersections

    def __calculate_rc(self, coord: Coordinate):
        rc = 0b0000

        if coord.x < -1:
            rc += 0b0001

        if coord.x > 1:
            rc += 0b0010

        if coord.y < -1:
            rc += 0b0100

        if coord.y > 1:
            rc += 0b1000

        return rc

    def __calculate_ac(self, line_coords):
        ac = (line_coords[1].y - line_coords[0].y) / (line_coords[1].x - line_coords[0].x)

        if ac == 0:
            raise ValueError("AC is zero!")

        return ac
