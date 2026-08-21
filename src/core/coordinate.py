from dataclasses import dataclass


@dataclass
class Coordinate:
    """
    Representa um par (x, y) puro -- sem identidade, nome ou tipo.

    Usado tanto para coordenadas de MUNDO (dentro de GraphicObject.coords)
    quanto para coordenadas de TELA (resultado de Viewport.transform).
    O significado depende de quem está segurando a instância, não da
    classe em si.
    """
    x: float
    y: float

    def __iter__(self):
        """Permite fazer x, y = coordinate."""
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"
