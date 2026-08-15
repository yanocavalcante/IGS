from PyQt6.QtWidgets import QApplication, QWidget


class SGIInterface(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Interactive Graphic System')
        self.show()
