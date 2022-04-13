#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Подключаемые модули
from PyQt5 import QtWidgets
import sys
# импорт сгенерированной фармы
from QtFormDeCoder import Ui_MainWindow
# и функционала
import WildcardCompression as wc

# Классы

class cWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Дополнительные настройки формы
        super(cWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(wc.listMethod)
        self.ui.comboBox.setCurrentIndex(wc.nMethodLZ77)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Код', 'Печать', 'Словарь'])
        self.ui.tableWidget.setColumnWidth(0, 40)
        self.ui.tableWidget.setColumnWidth(1, 144)
        self.ui.tableWidget.setColumnWidth(2, 144)
        self.ui.tableWidget.setRowCount(0)
        # подключение клик-сигнал к слоту btn1Clicked
        self.ui.pushButton1.clicked.connect(self.btn1Clicked)
        # подключение клик-сигнал к слоту btn2Clicked
        self.ui.pushButton2.clicked.connect(self.btn2Clicked)
        # а также установка параметров декодирования
        self.mDeCode = None
        pass

    def btn1Clicked(self):
        # Прочитаем выбранный метод сжатия
        nMethod = self.ui.comboBox.currentIndex()
        # Прочитаем сжатое сообщение
        tInputText = self.ui.lineEdit1.text()
        nInputText = len(tInputText)
        if nInputText == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Сжатое сообщение должно содержать хотя бы 1 символ!')
            msg.setDetailedText('Длина сжатого сообщения должна быть больше 0')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
        # Прочитаем размер словаря
        try:
            nDict = int(self.ui.lineEdit3.text().strip())
            if nDict > 36:
                nDict = 36
            elif nDict < 1:
                nDict = 1
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Размер словаря (в символах) должен быть натуральным числом!')
            msg.setDetailedText('Целое число, большее 0 (но не большее 36).')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            nDict = 8 # Значение по умолчанию
        finally:
            self.ui.lineEdit3.setText(str(nDict))
        # Установка параметров декодирования
        self.mDeCode = wc.makeDeCode(nMethod,tInputText,nDict)
        # Обнулим ход выполнения
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        # Очистим исходное соодщение
        self.ui.lineEdit2.setText('')
        return

    def btn2Clicked(self):
        # Если установка параметров декодирования не произведена
        if self.mDeCode == None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Нажмите кнопку "Начало(рестарт)"!')
            msg.setDetailedText('Установка параметров декодирования.')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
        # Создадим и запишем очередной код
        tCode, tDeCode = self.mDeCode.makeNextDeCode()
        # Если код пуст - достигли конца сообщения
        if tCode != '':
            # Запишем очередной шаг алгоритма
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            cellInfo = QtWidgets.QTableWidgetItem(tCode)
            self.ui.tableWidget.setItem(row, 0, cellInfo)
            cellInfo = QtWidgets.QTableWidgetItem(tDeCode)
            self.ui.tableWidget.setItem(row, 1, cellInfo)
            cellInfo = QtWidgets.QTableWidgetItem(self.mDeCode.tDict)
            self.ui.tableWidget.setItem(row, 2, cellInfo)
            # Запишем исходное соодщение
            self.ui.lineEdit2.setText(self.mDeCode.tOutputText)
        return

# -*- Main -*-
app = QtWidgets.QApplication([])
application = cWindow()
application.show()
sys.exit(app.exec())