
from pesistenseLayer.MatrixSaver import MatrixSaver

class Neuron(object):
    matrixSaver = MatrixSaver()

    name = None
    inputWeights = [[],[]]
    limit = 9

    lastResult = None
    lastInput = [[], []]

    def __init__(self, name):
        self.name = name
        self.extractWeights()

    def recognize(self, input):

    def punishNeuron(self):

    def extractWeights(self):
        if self.matrixSaver.hasFile(self.name):
            self.inputWeights = self.matrixSaver.loadMtrixFromFile(self.name)
        else:
            self.inputWeights = self.createRaudomInputWeights()
            self.saveWeights()

    def saveWeights(self):
        self.matrixSaver.saveMatrixInFile(self.name)


    def createRaudomInputWeights(self):
