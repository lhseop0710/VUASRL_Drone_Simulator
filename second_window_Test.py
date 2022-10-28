from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from mavsdk.mission import (MissionItem, MissionPlan)
# from  pablo_drone_uam_olyimpiad_test import WindowClass
from math import *
import re

chosen_points = []
mission_items = []

lat_zero = 47.4006681               #set default position
lon_zer0 = 8.5378115
lat_mapx = 0.0159811 / 1200
lon_mapy = 0.0060827 / 675

form_secondwindow = uic.loadUiType("second_window.ui")[0] #두 번째 창 ui
class secondwindow(QDialog, QWidget, form_secondwindow):

    def __init__(self):
        super().__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(1200,675)                        #창크기 고정
        self.show() #두번째창 실행
        self.setGeometry(10,10,1200,675)
        self.chosen_points = []
        self._image = QPixmap("pablo.png")
        self.pen_color = QColor.fromRgb(255,0,0)
        self.chosen_points = chosen_points


        # self.upate_timer = QTimer(self)
        # self.upate_timer.setInterval(10)  # milliseconds i believe
        # self.upate_timer.timeout(self.upate_label)
        # self.update_label()

    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle("VUASRL Ground Control System")

    def mouseReleaseEvent(self, cursor_event):
        global xy
        self.chosen_points.append(cursor_event.pos())
        self.update()

        mission_items.append(MissionItem(float(lat_zero) - (float(lon_mapy) * float(xy[1])),
                                         float(lon_zer0) + float(lat_mapx) * float(xy[0]),
                                         60,
                                         30,
                                         True,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan')))

        print(mission_items)

    def paintEvent(self, event):
        global points
        global xy
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self._image)
        path = QPainterPath()
        points = chosen_points

        # draw small red dots on each point
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QBrush(Qt.red))
        for i in range(len(points)):
            painter.drawEllipse(points[i], 3, 3)

        painter.setPen(QtCore.Qt.blue)
        painter.setBrush(QBrush(Qt.red, Qt.NoBrush)) #reset the brush
        path.moveTo(points[0])

        # connect the points with blue straight lines
        for i in range(len(points)-1):  # 1 less than length
           path.lineTo(points[i+1])

        for pos in self.chosen_points:
            pos_origin = str(pos).split("(")[1].split(")")[0]
            xy = pos_origin.split(', ')
            print(xy[0], xy[1])
        painter.drawPath(path)


    def close(self):
        self.close()
