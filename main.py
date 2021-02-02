from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


import sys
import requests
import os


class Map_Main(QWidget):
    def __init__(self):
        super(Map_Main, self).__init__()
        uic.loadUi('map.ui', self)
        self.findit.clicked.connect(self.set_map)

    def set_map(self):
        latitude = self.latit_inp.text()
        longitude = self.longit_inp.text()
        spn = self.spin.value()

        API_request = f'https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&spn={spn},{spn}&l=map&size=650,450'
        response = requests.get(API_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(API_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            map_file = 'map.png'

            with open(map_file, 'wb') as file:
                file.write(response.content)

        map_photo = QPixmap(map_file)
        map_photo = map_photo.scaled(1100, 790)
        self.map_line.setPixmap(map_photo)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map_Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
