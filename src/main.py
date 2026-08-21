import sys

from PyQt6.QtWidgets import QApplication

from controller.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.sgi.show()
    sys.exit(app.exec())
