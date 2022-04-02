from functools import partial

from IPython.core.inputtransformer2 import tr
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtGui import QImage
import io


from businessLogic.NeuralNetwork import NeuralNetwork
from pesistenseLayer.MatrixSaver import MatrixSaver

Form, _ = uic.loadUiType('face/form_gr.ui')


class Ui(QtWidgets.QMainWindow, Form):
    matrixSaver = MatrixSaver()
    neuralNetwork = None
    Image = None
    neuronNames = []

    placeWidth = 32
    placeHeight = 32


    drawing = False
    brushSize = 30

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.loadButton.clicked.connect(self.loadNueronNames)
        self.cleanPitureButton.clicked.connect(self.clean)
        self.savePictureButton.clicked.connect(self.savePicture)
        self.LoadPictureButton.clicked.connect(self.loadPicture)

        self.recognizeForLerningButton.clicked.connect(self.recognizeForLerning)
        self.punishButton.clicked.connect(self.punishNeuron)
        self.recognizeButton.clicked.connect(self.recognize)

        self.setWindowTitle("Однослойная нейронная сеть")

        self.canvas = QtGui.QPixmap(self.paintingLabel.size())
        self.canvas.fill(Qt.white)
        self.paintingLabel.setPixmap(self.canvas)
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        self.paintingLabel.mousePressEvent = self.mousePressEventForLabel
        self.paintingLabel.mouseMoveEvent = self.mouseMoveEventForLabel
        self.paintingLabel.mouseReleaseEvent = self.mouseReleaseEventForLabel


    def loadNueronNames(self):
        filePath, _ = QFileDialog.getOpenFileName(self,"Open file with names", "","text files (*.txt)")
        if filePath == "":
            return

        with open(filePath, encoding = 'utf-8') as f:
                self.neuronNames = ([f.readline().split()])[0]

        self.neuralNetwork = NeuralNetwork(self.neuronNames)
        self.resLoadSettingsLabel.setText("Создано " + str(len(self.neuronNames)) + " нейронов")
        self.comboBox.addItems(self.neuronNames)

    def clean(self):
        self.paintingLabel.setPixmap(self.canvas)
        self.pixMapToImage()
        self.printImage()

    def savePicture(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "BMP(*.bmp) ")

        if filePath == "":
            return

        if self.Image.save(filePath, quality=100) is True:
            QMessageBox.information(self, "Сохранение", "Файл успешно сохранен", QMessageBox.Ok)
        else:
            QMessageBox.Critical(self, "Сохранение", "Произошла ошибка при сохнарении", QMessageBox.Ok)

    def loadPicture(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "","BMP(*.bmp) ")
        if filePath == "":
            return
        self.pixMapToImage()
        self.printImage()


    def recognizeForLerning(self):
        neuronName = self.comboBox.currentText()
        neuronResult = self.neuralNetwork.getNeuronResult(neuronName, self.getMatrixFromImage())
        if neuronResult >= 1:
            self.resNeuronLabel.setText("верно")
            self.resNeuronLabel.setStyleSheet("color : green")
        else:
            self.resNeuronLabel.setText("не верно")
            self.resNeuronLabel.setStyleSheet("color : red")
        self.resNeuronLabel_2.setText("коэффициент точности: " + str(round(neuronResult, 2)))


    def punishNeuron(self):
        self.neuralNetwork.punishNeuron()

    def recognize(self):
        result, coef = self.neuralNetwork.recognize(self.getMatrixFromImage())
        if result is False:
            self.resNouralNetworkLabel.setText("Не распознано!")
            self.resNouralNetworkLabel.setStyleSheet("color : red")
        else:
            self.resNouralNetworkLabel.setText("На картинке изображена буква " + str(result))
            self.resNouralNetworkLabel.setStyleSheet("color : green")
            self.resNouralNetworkLabel_2.setStyleSheet("color : green")
            self.resNouralNetworkLabel_2.setText("C коэффициентом точности " + str(round(coef, 2)))

    def mousePressEventForLabel(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEventForLabel(self, e):
        if (e.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.paintingLabel.pixmap())
            print(self.brushColor, self.brushSize,
                  Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, e.pos())
            self.lastPoint = e.pos()
            self.update()

    def mouseReleaseEventForLabel(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

            self.pixMapToImage()
            self.printImage()

    def pixMapToImage(self):
        self.Image = self.paintingLabel.pixmap().toImage().\
            convertToFormat(QImage.Format_Mono, Qt.MonoOnly).scaled(self.placeWidth,self.placeHeight, transformMode=1)

    def printImage(self):
        pixmap = QtGui.QPixmap(self.Image)
        pixmap = pixmap.scaledToWidth(251)
        self.paintingLabel.setPixmap(pixmap)

    def getMatrixFromImage(self):
        matrix = [[0 for j in range(0, self.placeWidth)] for i in range(0, self.placeHeight)]
        for i in range(0, self.placeWidth):
            for j in range(0, self.placeHeight):
                if self.Image.pixelColor(i, j).getRgb() == (255, 255, 255, 255):
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = 1
        return matrix


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
