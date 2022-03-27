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
    placeForDrawing = [[],[]]
    neuronNames = []
    placeWidth = 5
    placeHeight = 7

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.loadButton.clicked.connect(self.loadNueronNames)
        self.initDrowingPlase()
        self.cleanPitureButton.clicked.connect(self.clean)
        self.savePictureButton.clicked.connect(self.savePicture)
        self.LoadPictureButton.clicked.connect(self.loadPicture)

        self.recognizeForLerningButton.clicked.connect(self.recognizeForLerning)
        self.punishButton.clicked.connect(self.punishNeuron)
        self.recognizeButton.clicked.connect(self.recognize)

        # self.pushButton_3.clicked.connect(self.clear)

    def initDrowingPlase(self):
        self.placeForDrawing = [[0 for j in range(0, self.placeWidth)] for i in range(0, self.placeHeight)]
        self.updateDrowingPlace()
        for i in range(self.placeWidth):
            for j in range(self.placeHeight):
                getattr(self, 'pushButton_' + str(j) + str(i)).clicked.connect(partial(self.drowingPlaseHandler,j,i))

    def drowingPlaseHandler(self,i,j):
        if self.placeForDrawing[i][j] == 1:
            self.placeForDrawing[i][j] = 0
        else:
            self.placeForDrawing[i][j] = 1

        self.updateDrowingPlace()

    def updateDrowingPlace(self):
        for i in range(self.placeWidth):
            for j in range(self.placeHeight):
                backgroundColor = "white"
                if self.placeForDrawing[j][i] == 1:
                    backgroundColor = "black"

                getattr(self, 'pushButton_' + str(j) + str(i)).setStyleSheet("background : " + backgroundColor)


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
        self.placeForDrawing = [[0 for j in range(0, self.placeWidth)] for i in range(0, self.placeHeight)]
        self.updateDrowingPlace()

    def savePicture(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Open Image", "", "text files (*.data)")
        if filePath == "":
            return

        if self.matrixSaver.savePicture(filePath, self.placeForDrawing) is True:
            QMessageBox.information(self, "Сохранение", "Файл успешно сохранен", QMessageBox.Ok)
        else:
            QMessageBox.Critical(self, "Сохранение", "Произошла ошибка при сохнарении", QMessageBox.Ok)


    def loadPicture(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "","text files (*.data)")
        if filePath == "":
            return

        if self.matrixSaver.checkFile(filePath) is False:
            QMessageBox.Critical(self, "Загрузка", "Файл не подходит", QMessageBox.Ok)
            return
        else:
            self.placeForDrawing = self.matrixSaver.loadPicture(filePath)
            self.updateDrowingPlace()
            QMessageBox.information(self, "Загрузка", "Файл успешно загружен", QMessageBox.Ok)


    def recognizeForLerning(self):
        neuronName = self.comboBox.currentText()
        neuronResult = self.neuralNetwork.getNeuronResult(neuronName, self.placeForDrawing)
        if neuronResult is True:
            self.resNeuronLabel.setText("верно")
            self.resNeuronLabel.setStyleSheet("color : green")
        else:
            self.resNeuronLabel.setText("не верно")
            self.resNeuronLabel.setStyleSheet("color : red")

    def punishNeuron(self):
        self.neuralNetwork.punishNeuron()

    def recognize(self):
        result = self.neuralNetwork.recognize(self.placeForDrawing)
        if result is False:
            self.resNouralNetworkLabel.setText("Не распознано!")
            self.resNouralNetworkLabel.setStyleSheet("color : red")
        else:
            self.resNouralNetworkLabel.setText("На картинке изображена буква " + str(result))
            self.resNouralNetworkLabel.setStyleSheet("color : green")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
