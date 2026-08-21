from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from view.dialogs.line_dialog import LineDialog
from view.dialogs.point_dialog import PointDialog
from view.dialogs.wireframe_dialog import WireframeDialog

_COORD_DIALOGS = {
    "Point": PointDialog,
    "Line": LineDialog,
    "Wireframe": WireframeDialog,
}

class CreateObjectDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Create New Object")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.__name = QLineEdit()
        self.__name.setPlaceholderText("e.g. MyFirstObject")
        form.addRow("Name:", self.__name)

        self.__type = QComboBox()
        self.__type.addItems(list(_COORD_DIALOGS.keys()))
        form.addRow("Type:", self.__type)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        self.__result: dict | None = None

    def get_object_dict(self) -> dict | None:
        if self.exec() != QDialog.DialogCode.Accepted:
            return None

        name = self.__name.text().strip()
        obj_type = self.__type.currentText()

        if not name:
            QMessageBox.warning(self, "IGS", "Set a name for the new object!")
            return None

        coord_dialog_class = _COORD_DIALOGS[obj_type]
        coord_dialog = coord_dialog_class(self.parent())

        if coord_dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        return {
            "Name": name,
            "Type": obj_type,
            "Coords": coord_dialog.get_coords(),
        }
