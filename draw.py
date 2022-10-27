from PyQt5 import QtWidgets, QtGui, QtCore, uic

class WayPoints_Creator(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(10,10,1200,675)
        self.chosen_points = []
        self._image = QtGui.QPixmap("pablo.png")
        self.pen_color = QtGui.QColor.fromRgb(255,0,0)

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._image)
        print(self.rect)
        # self.rect().setRect(10,10,1200,675)
        pen = QtGui.QPen()
        pen.setColor(self.pen_color)
        pen.setWidth(10)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        for pos in self.chosen_points:
            painter.drawPoint(pos)
            print(pos)

    def mouseReleaseEvent(self, cursor_event):
        self.chosen_points.append(cursor_event.pos())
        # self.chosen_points.append(self.mapFromGlobal(QtGui.QCursor.pos()))
        self.update()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = WayPoints_Creator()
    w.show()
    sys.exit(app.exec_())