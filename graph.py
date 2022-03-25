from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QImage

Form, _ = uic.loadUiType('form_gr.ui')


class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        # self.canvas = QtGui.QPixmap(self.label.size())
        # self.canvas.fill(Qt.white)
        # self.label.setPixmap(self.canvas)
        self.drawing = False
        self.brushColor = Qt.black
        self.brushSize = 3
        self.lastPoint = QPoint()
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.clear)
        # self.horizontalSlider.valueChanged.connect(self.bruh)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.label.pixmap())
            print(self.brushColor, self.brushSize,
                  Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, e.pos())
            self.lastPoint = e.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def bruh(self, n):
        self.brushSize = 50

    def clear(self):
        self.label.setPixmap(self.canvas)

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        im = self.label.pixmap().toImage().convertToFormat(QImage.Format_Mono, Qt.MonoOnly).scaled(33,33, transformMode=1)
        for i in range(0,32):
            for j in range(0,32):
                if im.pixelColor(i,j).getRgb() != (255,255,255,255):
                    im.setPixelColor(i,j, QtGui.QColor(0, 0, 0,255))
        im.save(filePath, quality=100)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
