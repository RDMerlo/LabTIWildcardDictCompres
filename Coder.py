#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Подключаемые модули
from PyQt5 import QtWidgets
import sys

# импорт сгенерированной фармы
from QtFormCoder import Ui_MainWindow
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
        self.ui.tableWidget.setHorizontalHeaderLabels(['Словарь', 'Буфер', 'Код'])
        self.ui.tableWidget.setColumnWidth(0, 144)
        self.ui.tableWidget.setColumnWidth(1, 144)
        self.ui.tableWidget.setColumnWidth(2, 40)
        self.ui.tableWidget.setRowCount(0)
        # подключение клик-сигнал к слоту btn1Clicked
        self.ui.pushButton1.clicked.connect(self.btn1Clicked)
        # подключение клик-сигнал к слоту btn2Clicked
        self.ui.pushButton2.clicked.connect(self.btn2Clicked)
        # а также установка параметров кодирования
        self.mCode = None
        pass

    def btn1Clicked(self):
        # Прочитаем выбранный метод сжатия
        nMethod = self.ui.comboBox.currentIndex()
        # Прочитаем исходное сообщение
        tInputText = self.ui.lineEdit1.text()
        nInputText = len(tInputText)
        if nInputText == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Исходное сообщение должно содержать хотя бы 1 символ!')
            msg.setDetailedText('Длина исходного сообщения должна быть больше 0')
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
        # Прочитаем размер буфера
        try:
            nBuff = int(self.ui.lineEdit4.text().strip())
            if nBuff > 36:
                nBuff = 36
            elif nBuff < 1:
                nBuff = 1
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Размер буфера (в символах) должен быть натуральным числом!')
            msg.setDetailedText('Целое число, большее 0 (но не большее 36).')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            nBuff = 5 # Значение по умолчанию
        finally:
            self.ui.lineEdit4.setText(str(nBuff))
        # Установка параметров кодирования
        self.mCode = wc.makeCode(nMethod,tInputText,nDict,nBuff)
        # Обнулим ход выполнения
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        # Очистим сжатое соодщение
        self.ui.lineEdit2.setText('')
        # а также длину сжатого сообщения и коэффициент сжатия
        self.ui.lineEdit5.setText('0')
        self.ui.lineEdit6.setText('0')
        return

    def btn2Clicked(self):
        # Если установка параметров кодирования не произведена
        if self.mCode == None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Информация')
            msg.setText('Нажмите кнопку "Начало(рестарт)"!')
            msg.setDetailedText('Установка параметров кодирования.')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
        # Создадим и запишем очередной код
        tDict, tBuff, tCode = self.mCode.makeNextCode()
        # Если код пуст - достигли конца сообщения
        if tCode != '':
            # Запишем очередной шаг алгоритма
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            cellInfo = QtWidgets.QTableWidgetItem(tDict)
            self.ui.tableWidget.setItem(row, 0, cellInfo)
            cellInfo = QtWidgets.QTableWidgetItem(tBuff)
            self.ui.tableWidget.setItem(row, 1, cellInfo)
            cellInfo = QtWidgets.QTableWidgetItem(tCode)
            self.ui.tableWidget.setItem(row, 2, cellInfo)
            # Запишем сжатое соодщение
            self.ui.lineEdit2.setText(self.mCode.tOutputText)
            # а также длину сжатого сообщения и коэффициент сжатия
            self.ui.lineEdit5.setText(str(self.mCode.sizeOutputText))
            self.ui.lineEdit6.setText(str(self.mCode.sizeOutputText/(len(self.mCode.tInputText)*wc.sizeSymbol)))
        return

# -*- Main -*-

app = QtWidgets.QApplication([])
application = cWindow()
application.show()
sys.exit(app.exec())