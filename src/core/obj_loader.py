from core.coordinate import Coordinate


class ObjLoader:
    """
    Loads wireframe models from Wavefront .obj files.

    Supported statements:
      v x y z [w]      vertex (w is ignored)
      l i j k ...      polyline: edges (i, j), (j, k), ...
      f i j k ...      face: its boundary edges (closed), shared edges kept once
    Indices are 1-based; negative indices are relative to the vertices read
    so far. Entries such as "i/t/n" use only the vertex index. Any other
    statement (o, g, vt, vn, s, usemtl, mtllib, ...) and comments are ignored.

    [IAGen] Class generated with the help of an LLM (see AIGen.md).
    """

    @staticmethod
    def load(path: str) -> tuple[list[Coordinate], list[tuple[int, int]]]:
        with open(path, "r", encoding="utf-8") as file:
            return ObjLoader.parse(file.read())

    @staticmethod
    def parse(text: str) -> tuple[list[Coordinate], list[tuple[int, int]]]:
        vertices: list[Coordinate] = []
        edges: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()

        def add_edge(a: int, b: int) -> None:
            key = (min(a, b), max(a, b))
            if a != b and key not in seen:
                seen.add(key)
                edges.append((a, b))

        for number, line in enumerate(text.splitlines(), start=1):
            tokens = line.split("#", 1)[0].split()
            if not tokens:
                continue

            keyword, args = tokens[0], tokens[1:]

            try:
                if keyword == "v":
                    if len(args) < 3:
                        raise ValueError("a vertex needs x, y and z")
                    vertices.append(Coordinate(*(float(value) for value in args[:3])))

                elif keyword in ("l", "f"):
                    if len(args) < 2:
                        raise ValueError("needs at least two vertex indices")
                    indices = [ObjLoader.__resolve(arg, len(vertices)) for arg in args]
                    pairs = list(zip(indices, indices[1:]))
                    if keyword == "f":
                        pairs.append((indices[-1], indices[0]))
                    for a, b in pairs:
                        add_edge(a, b)
            except ValueError as error:
                raise ValueError(f"line {number}: {error}") from None

        if len(vertices) < 2 or not edges:
            raise ValueError("the file must define at least two vertices and one edge (l or f)")

        if max(max(edge) for edge in edges) >= len(vertices):
            raise ValueError("an edge references a vertex that is never defined")

        return vertices, edges

    @staticmethod
    def load_bezier_surface(path: str) -> list[Coordinate]:
        with open(path, "r", encoding="utf-8") as file:
            return ObjLoader.parse_bezier_surface(file.read())

    @staticmethod
    def parse_bezier_surface(text: str) -> list[Coordinate]:
        patches: list[list[Coordinate]] = []
        current: list[Coordinate] = []
        has_delimiters = False

        def finish_patch(line_number: int) -> None:
            nonlocal current
            if not current:
                return
            if len(current) != 16:
                raise ValueError(f"line {line_number}: each Bézier patch must have exactly 16 vertices")
            patches.append(current)
            current = []

        for number, line in enumerate(text.splitlines(), start=1):
            tokens = line.split("#", 1)[0].split()
            if not tokens:
                continue
            keyword, args = tokens[0], tokens[1:]
            if keyword in ("o", "g"):
                has_delimiters = True
                finish_patch(number)
                continue
            if keyword != "v":
                continue
            if len(args) < 3:
                raise ValueError(f"line {number}: a vertex needs x, y and z")
            try:
                current.append(Coordinate(*(float(value) for value in args[:3])))
            except ValueError:
                raise ValueError(f"line {number}: invalid vertex coordinates") from None
            if not has_delimiters and len(current) == 16:
                patches.append(current)
                current = []

        finish_patch(number if text else 1)
        if not patches:
            raise ValueError("the file must define at least one Bézier patch with 16 vertices")
        return [point for patch in patches for point in patch]

    @staticmethod
    def __resolve(token: str, vertex_count: int) -> int:
        index = int(token.split("/", 1)[0])

        if index > 0:
            return index - 1
        if index < 0 and -index <= vertex_count:
            return vertex_count + index

        raise ValueError(f"invalid vertex index {token!r}")
