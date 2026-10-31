import re

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLabel, QMessageBox,
    QPlainTextEdit, QVBoxLayout,
)

from core.coordinate import Coordinate


class BezierSurfaceDialog(QDialog):
    """Input dialog for one or more 4x4 bicubic Bézier control meshes."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Bézier Surface Control Points")
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__patches_field = QPlainTextEdit()
        self.__patches_field.setPlaceholderText(
            "(x11,y11,z11),(x12,y12,z12),(x13,y13,z13),(x14,y14,z14);\n"
            "(x21,y21,z21),(x22,y22,z22),(x23,y23,z23),(x24,y24,z24);\n"
            "(x31,y31,z31),(x32,y32,z32),(x33,y33,z33),(x34,y34,z34);\n"
            "(x41,y41,z41),(x42,y42,z42),(x43,y43,z43),(x44,y44,z44)"
        )
        self.__patches_field.setMinimumHeight(170)
        form.addRow("Control meshes:", self.__patches_field)
        layout.addLayout(form)
        layout.addWidget(QLabel(
            "Use ';' between the 4 rows of a patch and '|' between patches. "
            "Each row must contain exactly 4 points in the form (x,y,z)."
        ))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.__try_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.__coords: list[Coordinate] = []

    def __try_accept(self) -> None:
        try:
            self.__coords = self.__parse(self.__patches_field.toPlainText())
            self.accept()
        except ValueError as error:
            QMessageBox.warning(self, "Invalid input", str(error))

    @staticmethod
    def __parse(text: str) -> list[Coordinate]:
        number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
        point = re.compile(rf"\(\s*({number})\s*,\s*({number})\s*,\s*({number})\s*\)")
        patches = text.split("|")
        if not text.strip() or any(not patch.strip() for patch in patches):
            raise ValueError("Provide at least one patch; use '|' only between patches.")

        coords: list[Coordinate] = []
        for patch_number, patch in enumerate(patches, start=1):
            rows = [row.strip() for row in patch.split(";") if row.strip()]
            if len(rows) != 4:
                raise ValueError(f"Patch {patch_number} must contain exactly 4 rows separated by ';'.")
            for row_number, row in enumerate(rows, start=1):
                matches = list(point.finditer(row))
                leftover = point.sub("", row)
                if len(matches) != 4 or re.sub(r"[\s,]", "", leftover):
                    raise ValueError(
                        f"Patch {patch_number}, row {row_number} must contain exactly 4 points as (x,y,z)."
                    )
                coords.extend(Coordinate(*(float(value) for value in match.groups())) for match in matches)
        return coords

    def get_coords(self) -> list[Coordinate]:
        return self.__coords
