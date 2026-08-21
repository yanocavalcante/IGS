from core.coordinate import Coordinate
from core.viewport import Viewport
from core.window import Window
from models.display_file import DisplayFile
from models.graphic_obj import GraphicObject
from models.line import Line
from models.obj_type import ObjectType
from models.point import Point
from models.wireframe import Wireframe
from view.interface import SGIInterface

# Tabela de despacho: nome escolhido na UI -> (classe concreta, ObjectType)
# Para adicionar um novo tipo de objeto no futuro (ex: Curve), basta
# adicionar uma linha aqui -- nada mais no Controller muda.
_TYPE_MAP: dict[str, tuple[type[GraphicObject], ObjectType]] = {
    "Point": (Point, ObjectType.POINT),
    "Line": (Line, ObjectType.LINE),
    "Wireframe": (Wireframe, ObjectType.WIREFRAME),
}


class Controller:
    """
    Mediador entre View e o "motor" gráfico.

    É o único componente que conhece DisplayFile, Window e Viewport
    ao mesmo tempo. Recebe intenções da View (criar objeto, pan, zoom)
    e devolve à View o que precisa ser desenhado, já transformado
    para coordenadas de tela.
    """

    def __init__(self) -> None:
        self.display_file = DisplayFile()
        self.window = Window(0, 0, 600, 400)
        self.viewport = Viewport(0, 0, 600, 400)
        self.sgi = SGIInterface(self)

    # ---- criação de objetos -------------------------------------------------

    def add_object(self, obj_dict: dict) -> None:
        """
        obj_dict esperado:
        {
            "Name": str,
            "Type": "Point" | "Line" | "Wireframe",
            "Coords": list[Coordinate],
        }
        """
        obj_class, obj_type = _TYPE_MAP[obj_dict["Type"]]
        self.display_file.add(obj_class, obj_type, obj_dict["Name"], obj_dict["Coords"])
        self.sgi.refresh_canvas()

    def remove_object(self, obj_id: int) -> None:
        self.display_file.remove(obj_id)
        self.sgi.refresh_canvas()

    # ---- navegação e zoom -----------------------------------------------------

    def pan(self, dx: float, dy: float) -> None:
        self.window.pan(dx, dy)
        self.sgi.refresh_canvas()

    def zoom(self, factor: float) -> None:
        self.window.zoom(factor)
        self.sgi.refresh_canvas()

    # ---- pipeline de desenho ---------------------------------------------------

    def get_drawable_objects(self) -> list[tuple[GraphicObject, list[Coordinate]]]:
        """
        Para cada objeto do DisplayFile (visível ou não), calcula suas
        coordenadas de tela segundo a Window atual. O Canvas só desenha
        o que este método devolve -- ele nunca acessa DisplayFile direto.
        """
        return [
            (obj, self.viewport.transform_all(obj.coords, self.window))
            for obj in self.display_file.objects
        ]
