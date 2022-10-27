#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtSvg

from threadGUI import ThreadGUI
from PyQt5.QtCore import QTimer
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC
import math
import time
from PyQt5.QtCore import QTimer
from datetime import datetime
import  serial
import serial.tools.list_ports

i=0

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("Stm Real Time Simulator")

        self.mainLayout=QVBoxLayout()
        self.upLayout=QFormLayout()
        self.layout=QGridLayout()

        self.mainLayout.addLayout(self.upLayout,30)
        self.mainLayout.addLayout(self.layout,70)

        self.port_label=QLabel("Port :")
        self.port=QComboBox()
        self.port.setStyleSheet("font-size:8pt;")
        self.list_port()
        self.frequency_label=QLabel("Frequency(Hz) :")
        self.frequency=QLineEdit()
        self.baudrate_label=QLabel("BaudRate :")
        self.baudrate=QComboBox()
        self.baudrate.addItems(["9600"])
        self.pitch=QLabel("Pitch :  ")
        self.pitch_value=QLabel("...")
        self.pitch.setStyleSheet("color:red;")
        self.pitch_value.setStyleSheet("color:red;")
        self.roll=QLabel("Roll :  ")
        self.roll_value=QLabel("...")
        self.roll.setStyleSheet("color:green;")
        self.roll_value.setStyleSheet("color:green;")

        self.btn_connect=QPushButton("Enter",self)
        self.btn_connect.clicked.connect(self.connect_system)
        
        self.btn_exit=QPushButton("Exit",self)
        self.btn_exit.clicked.connect(self.exit)

        self.upLayout.addRow(self.port_label,self.port)
        self.upLayout.addRow(self.baudrate_label,self.baudrate)
        self.upLayout.addRow(self.frequency_label,self.frequency)
        self.upLayout.addRow(self.btn_connect,self.btn_exit)
        self.upLayout.addRow(self.pitch,self.pitch_value)
        self.upLayout.addRow(self.roll,self.roll_value)
        
        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(300, 300)
        self.adi.reinit()
        self.layout.addWidget(self.adi, 0, 0)

        self.setLayout(self.mainLayout)
        
        self.timer=QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update1)
        self.show()

    def update1(self):
        global i
        line = str(self.ser.readline())
        print(line)
        data = line.split(",")
        print(data)
        self.pitch_value.setText(str(data[1]))
        self.roll_value.setText(str(data[2]))
        self.adi.setRoll(float(data[1]))
        self.adi.setPitch(float(data[2]))
        self.adi.viewUpdate.emit()
        
    def connect_system(self):
        print("Connecting System")
        self.ser = serial.Serial(self.port.currentText(), 9600)
        print(str(self.port)+" Connecting Port")
        self.timer.start()

    def list_port(self):
        ports = list(serial.tools.list_ports.comports())
        print(ports)
        for p in ports:
            print(p)
            self.port.addItems(p)

    def exit(self):
        self.timer.stop()
        sys.exit()
        

    
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

