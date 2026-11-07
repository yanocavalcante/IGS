import re

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLabel, QMessageBox,
    QPlainTextEdit, QVBoxLayout,
)

from core.coordinate import Coordinate


class BSplineSurfaceDialog(QDialog):
    """Input dialog for a 4x4 to 20x20 cubic B-spline control matrix."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("B-Spline Surface Control Points")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.__matrix_field = QPlainTextEdit()
        self.__matrix_field.setPlaceholderText(
            "(x11,y11,z11),(x12,y12,z12),...;(x21,y21,z21),(x22,y22,z22),...;..."
        )
        self.__matrix_field.setMinimumHeight(170)
        form.addRow("Control matrix:", self.__matrix_field)
        layout.addLayout(form)
        layout.addWidget(QLabel(
            "Separate rows with ';'. Each row must have the same number of points; "
            "the matrix must be between 4x4 and 20x20."
        ))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.__try_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.__coords: list[Coordinate] = []
        self.__rows = 0
        self.__cols = 0

    def __try_accept(self) -> None:
        try:
            self.__coords, self.__rows, self.__cols = self.__parse(self.__matrix_field.toPlainText())
            self.accept()
        except ValueError as error:
            QMessageBox.warning(self, "Invalid input", str(error))

    @staticmethod
    def __parse(text: str) -> tuple[list[Coordinate], int, int]:
        number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
        point = re.compile(rf"\(\s*({number})\s*,\s*({number})\s*,\s*({number})\s*\)")
        rows = [row.strip() for row in text.split(";")]
        if not text.strip() or any(not row for row in rows):
            raise ValueError("Provide rows separated by ';' without empty rows.")
        if not 4 <= len(rows) <= 20:
            raise ValueError("The control matrix must have from 4 to 20 rows.")

        matrix: list[list[Coordinate]] = []
        for row_number, row in enumerate(rows, start=1):
            matches = list(point.finditer(row))
            leftover = point.sub("", row)
            if not matches or re.sub(r"[\s,]", "", leftover):
                raise ValueError(f"Row {row_number} must contain points in the form (x,y,z).")
            matrix.append([Coordinate(*(float(value) for value in match.groups())) for match in matches])

        cols = len(matrix[0])
        if not 4 <= cols <= 20:
            raise ValueError("Each row must have from 4 to 20 points.")
        if any(len(row) != cols for row in matrix):
            raise ValueError("All rows of the control matrix must have the same number of points.")
        return [point for row in matrix for point in row], len(matrix), cols

    def get_coords(self) -> list[Coordinate]:
        return self.__coords

    def get_dimensions(self) -> tuple[int, int]:
        return self.__rows, self.__cols
