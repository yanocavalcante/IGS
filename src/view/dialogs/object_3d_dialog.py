from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QMessageBox, QVBoxLayout
from core.coordinate import Coordinate


class Object3DDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("3D Object")
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__vertices_field = QLineEdit()
        self.__vertices_field.setPlaceholderText("e.g. 0,0,0; 100,0,0; 100,100,0")
        form.addRow("Vertices:", self.__vertices_field)
        self.__edges_field = QLineEdit()
        self.__edges_field.setPlaceholderText("e.g. 0,1; 1,2; 2,0")
        form.addRow("Edges:", self.__edges_field)
        layout.addLayout(form)
        layout.addWidget(QLabel("Edges use the zero-based indices of the vertices."))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.__try_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.__coords: list[Coordinate] = []
        self.__edges: list[tuple[int, int]] = []

    def __try_accept(self) -> None:
        try:
            coords = self.__parse_vertices(self.__vertices_field.text())
            edges = self.__parse_edges(self.__edges_field.text())
            if len(coords) < 2 or not edges:
                raise ValueError("Provide at least two vertices and one edge.")
            
            if any(min(edge) < 0 or max(edge) >= len(coords) for edge in edges):
                raise ValueError("Each edge must reference an existing vertex.")
            
            self.__coords, self.__edges = coords, edges
            self.accept()
        except ValueError as error:
            QMessageBox.warning(self, "Invalid input", str(error))

    @staticmethod
    def __parse_vertices(text: str) -> list[Coordinate]:
        vertices = []
        for chunk in text.split(";"):
            if not chunk.strip():
                continue
            values = chunk.strip().split(",")
            if len(values) != 3:
                raise ValueError("Each vertex must have x, y and z coordinates.")
            vertices.append(Coordinate(*(float(value) for value in values)))
        return vertices

    @staticmethod
    def __parse_edges(text: str) -> list[tuple[int, int]]:
        edges = []
        for chunk in text.split(";"):
            if not chunk.strip():
                continue
            values = chunk.strip().split(",")
            if len(values) != 2:
                raise ValueError("Each edge must contain exactly two indices.")
            edges.append((int(values[0]), int(values[1])))
        return edges

    def get_coords(self) -> list[Coordinate]:
        return self.__coords

    def get_edges(self) -> list[tuple[int, int]]:
        return self.__edges
