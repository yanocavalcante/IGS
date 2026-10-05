from dataclasses import dataclass
from vertex import Vertex


@dataclass
class Edge:
    start: Vertex
    end: Vertex
