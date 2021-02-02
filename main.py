from PyQt5.QtWidgets import *
from PyQt5 import uic


import sys


class Map_Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('map.ui', self)
        self.findit.clicked.connect(self.set_map)

    def set_map(self):
        request_api()

    def request_api(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
