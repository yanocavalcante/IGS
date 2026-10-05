from dataclasses import dataclass
from vertex import Vertex
from edge import Edge


@dataclass
class Face:
    vertexes: list[Vertex]
    edges: list[Edge]
