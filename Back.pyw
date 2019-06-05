from Front import *
from images_rc import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, sqlite3



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, *args, **kwargs):
        
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.google.hide()
        self.hide = True
        self.mapa.hide()
        self.direccion.hide()
        self.circuito.hide()
        self.departamento.hide()
        self.label_direccion.hide()
        self.label_circuito.hide()
        self.label_departamento.hide()
        self.buscar.clicked.connect(self.query)
        self.mapa.clicked.connect(self.map)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.crono)
        timer.start(1000)
        self.crono()


    def query(self):

        try:
            bd = sqlite3.connect("db")
            cursor = bd.cursor()
            serie = self.serie.text().upper()
            try:
                if len(self.serie.text()) == 3:
                    pass
                else:
                    raise Exception
                numero = int(self.numero.text())
            except Exception as e:
                print(e)
                return self.label_alerta.setText("CREDENCIAL INVALIDA")
            sentencia = f"SELECT ur, circuito, lld FROM padron WHERE serie = '{serie}' AND desde <= {numero} AND hasta >= {numero}"
            cursor.execute(sentencia)
            res = cursor.fetchall()
            sentencia = f"SELECT departamento FROM departamentos WHERE serie = '{serie[0]}'"
            cursor.execute(sentencia)
            dep = cursor.fetchall()
            self.dep = dep
            if len(res) > 0:
                self.departamento.setText("{} ({})".format(dep[0][0], str(res[0][0])))
                self.circuito.setText(str(res[0][1]))
                self.direccion.setText(str(res[0][2]).capitalize())
                self.mapa.show()
                self.direccion.show()
                self.circuito.show()
                self.departamento.show()
                self.label_direccion.show()
                self.label_circuito.show()
                self.label_departamento.show()
                self.label_alerta.setText("")
            else:
                self.label_alerta.setText("CREDENCIAL NO EXISTE")
            bd.close()
        except Exception as e:
            self.label_alerta.setText("SE PRODUJO UN ERROR")
            print(e)
            bd.close()

        
    def map(self):

        try:
            URL = 'https://www.google.com/maps/place/Uruguay,"{}","{}"'.format(self.dep[0][0], self.direccion.text())
            self.google.load(QtCore.QUrl(URL))
            if self.hide == True:
                self.google.show()
                self.mapa.setText("CERRAR MAPA")
                self.hide = False
            else:
                self.google.hide()
                self.mapa.setText("VER MAPA")
                self.hide = True
        except Exception as e:
            self.label_alerta.setText("ERROR ABRIENDO MAPA")
            print(e)


    def crono(self):
        fecha = QtCore.QDate.currentDate()
        if QtCore.QDate.month(fecha) <= 6 and QtCore.QDate.year(fecha) == 2019:
            fecha_elec = QtCore.QDate(2019, 6, 30)
            self.label_regresiva.setText('Cuenta Regresiva para las Internas')
        elif ((6 < QtCore.QDate.month(fecha) < 10) or (QtCore.QDate.month(fecha) == 10 and QtCore.QDate.day(fecha) <= 27)) and QtCore.QDate.year(fecha) == 2019:
            fecha_elec = QtCore.QDate(2019, 10, 27)
            self.label_regresiva.setText('Cuenta Regresiva para las Primarias')
        elif ((QtCore.QDate.day(fecha) <= 24 and QtCore.QDate.month(fecha) == 11) or (QtCore.QDate.day(fecha) > 27 and QtCore.QDate.month(fecha) == 10)) and QtCore.QDate.year(fecha) == 2019:
            fecha_elec = QtCore.QDate(2019, 11, 24)
            self.label_regresiva.setText('Cuenta Regresiva para la Segunda Vuelta')
        else:
            fecha_elec = QtCore.QDate(2020, 5, 30)
            self.label_regresiva.setText('LAS ELECCIONES HAN FINALIZADO')
        hora = QtCore.QTime.currentTime()
        dias = QtCore.QDate.daysTo(fecha, fecha_elec) * 24
        horas = dias + 23 - QtCore.QTime.hour(hora)
        minutos = 59 - QtCore.QTime.minute(hora)
        segundos = 59 - QtCore.QTime.second(hora)
        if dias >= 0:
            self.lcd.display('{:0=4d}:{:0=2d}:{:0=2d}'.format(horas, minutos, segundos))
        else:
            self.lcd.display(f'{"f1hal12ado"}')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
