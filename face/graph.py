from IPython.core.inputtransformer2 import tr
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QImage

from businessLogic.NeuralNetwork import NeuralNetwork

Form, _ = uic.loadUiType('face/form_gr.ui')


class Ui(QtWidgets.QMainWindow, Form):
    neuralNetwork = None

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.loadButton.clicked.connect(self.loadNueronNames)
        # self.pushButton_3.clicked.connect(self.clear)

    def loadNueronNames(self):
        names = []

        filePath, _ = QFileDialog.getOpenFileName(self,"Open Image", "","text files (*.txt)")
        if filePath == "":
            return

        with open(filePath, encoding = 'utf-8') as f:
            for line in f:
                names.append([line.split()])

        self.neuralNetwork = NeuralNetwork(names)

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
