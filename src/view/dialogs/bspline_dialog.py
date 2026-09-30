import re

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)
from core.coordinate import Coordinate


class BSplineDialog(QDialog):
    """
    Diálogo para entrada dos pontos de controle de uma curva B-Spline.

    O input segue o padrão de especificação de objetos:
    (x1,y1),(x2,y2),... com, no mínimo, 4 pontos de controle.

    [IAGen] Implementação desta classe e de seus métodos gerada com auxílio
    de LLM (ver AIGen.md).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("B-Spline Control Points")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__coords_field = QLineEdit()
        self.__coords_field.setPlaceholderText("e.g. (10,10),(20,50),(40,20),(60,60)")
        form.addRow("Control points:", self.__coords_field)
        layout.addWidget(QLabel("Input control points as (x1,y1),(x2,y2),... with a minimum of 4 points"))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.__try_accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        self.__coords: list[Coordinate] = []

    def __try_accept(self) -> None:
        try:
            coords = self.__parse(self.__coords_field.text())
            if len(coords) < 4:
                raise ValueError("A B-Spline needs, at least, 4 control points.")
            self.__coords = coords
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid input", str(e))

    @staticmethod
    def __parse(text: str) -> list[Coordinate]:
        """
        Extrai pontos do texto no formato (x1,y1),(x2,y2),...

        Valores numéricos são aceitos como inteiros ou decimais, com ou sem
        sinal.

        [IAGen] Trecho gerado com auxílio de LLM (ver AIGen.md).
        """
        pattern = r"\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)"
        matches = re.findall(pattern, text)

        if not matches:
            raise ValueError("Invalid format. Use (x1,y1),(x2,y2),...")

        return [Coordinate(float(x), float(y)) for x, y in matches]

    def get_coords(self) -> list[Coordinate]:
        return self.__coords