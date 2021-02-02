"""
This application is a training work on WEB-7 " WEB. Знакомство с API" and pretends that this is a fucking cool map (no).
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic

import sys
import requests


class Main(QWidget):
    def __init__(self):
        """
        Initialized a program.
        """
        super(Main, self).__init__()
        uic.loadUi('map.ui', self)

        # Костыль
        self.type_of_map.setEditable(True)
        self.type_of_map.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.type_of_map.setEditable(False)

        # setup map and connect buttons
        self.set_map()
        self.findit.clicked.connect(self.set_map)
        self.resetit.clicked.connect(self.reset_map)

    def set_map(self):
        """
        Setup map.
        :return: no returns
        """
        self.api_req()

        map_photo = QPixmap(self.map_file)
        map_photo = map_photo.scaled(1100, 790)
        self.map_line.setPixmap(map_photo)

        self.get_address()

    def reset_map(self):
        """
        Returns the map settings to constant values.
        :return: no returns
        """
        file = open('config.cfg')  # open configuration
        data = file.read()
        data = data.split('\n')
        self.latit_inp.setText(data[0])
        self.longit_inp.setText(data[1])
        self.spin.setValue(float(data[2]))
        self.point_to_find.setText('')
        self.full_address.setText('')

        self.set_map()

    def api_req(self):
        """
        Generates an API request from the available input and generates a map to the output.
        :return: no returns
        """
        if self.point_to_find.text() == '':
            latitude = self.latit_inp.text()
            longitude = self.longit_inp.text()
            spn = self.spin.value()
        else:
            point = self.point_to_find.text()
            API_request = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={point}&format=json'
            response = requests.get(API_request)

            if not response:
                print('Ошибка выполнения запроса:')
                print(API_request)
                print('Http статус:', response.status_code, '(', response.reason, ')')
                sys.exit(1)
            else:
                json_response = response.json()
                toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                toponym_coodrinates = toponym['Point']['pos']
                latitude, longitude = toponym_coodrinates.split(' ')
                self.latit_inp.setText(latitude)
                self.longit_inp.setText(longitude)
                spn = self.spin.value()

        types = {
            'Режим "Карта"': 'map',
            'Режим "Спутник"': 'sat',
            'Режим "Гибрид"': 'sat,skl'
        }

        API_request = f'https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&spn={spn},{spn}&l=' \
                      f'{types[self.type_of_map.currentText()]}&size=650,450&pt={latitude},{longitude},flag'
        response = requests.get(API_request)

        if not response:
            print('Ошибка выполнения запроса:')
            print(API_request)
            print('Http статус:', response.status_code, '(', response.reason, ')')
            sys.exit(1)
        else:
            self.map_file = 'map.png'

            with open(self.map_file, 'wb') as file:
                file.write(response.content)

    def get_address(self):
        if self.point_to_find.text() == '':
            pass
        else:
            point = self.point_to_find.text()
            API_request = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={point}&format=json'
            response = requests.get(API_request)

            if not response:
                print('Ошибка выполнения запроса:')
                print(API_request)
                print('Http статус:', response.status_code, '(', response.reason, ')')
                sys.exit(1)
            else:
                json_response = response.json()

                toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
                self.full_address.setText(f'Полный адрес места: {toponym_address}')

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
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
