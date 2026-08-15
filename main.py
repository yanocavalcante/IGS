from interface import SGIInterface, QApplication
import sys


if __name__ == '__main__':
    sgi = QApplication(sys.argv)
    window = SGIInterface()
    sys.exit(sgi.exec())
