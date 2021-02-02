from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic


import sys
import requests
import os


class Map_Main(QWidget):
    def __init__(self):
        super(Map_Main, self).__init__()
        uic.loadUi('map.ui', self)

        self.type_of_map.setEditable(True)
        self.type_of_map.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.type_of_map.setEditable(False)

        self.set_map()
        self.findit.clicked.connect(self.set_map)

    def set_map(self):
        self.api_req()

        map_photo = QPixmap(self.map_file)
        map_photo = map_photo.scaled(1100, 790)
        self.map_line.setPixmap(map_photo)

    def api_req(self):
        latitude = self.latit_inp.text()
        longitude = self.longit_inp.text()
        spn = self.spin.value()

        types = {
            'Режим "Карта"': 'map',
            'Режим "Спутник"': 'sat',
            'Режим "Гибрид"': 'sat,skl'
        }

        API_request = f'https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&spn={spn},{spn}&l={types[self.type_of_map.currentText()]}&size=650,450'
        response = requests.get(API_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(API_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            self.map_file = 'map.png'

            with open(self.map_file, 'wb') as file:
                file.write(response.content)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            spn = self.spin.setValue(self.spin.value() + 0.05)
            self.set_map()
        elif event.key() == QtCore.Qt.Key_PageDown:
            spn = self.spin.setValue(self.spin.value() - 0.05)
            self.set_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map_Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
