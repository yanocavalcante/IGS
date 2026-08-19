from controller import Controller
from interface import SGIInterface, QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    window = controller.sgi
    window.show()
    sys.exit(app.exec())
