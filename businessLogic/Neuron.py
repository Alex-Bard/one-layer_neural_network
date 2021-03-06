from pesistenseLayer.MatrixSaver import MatrixSaver
import random

class Neuron(object):
    matrixSaver = MatrixSaver()

    name = None
    inputWeights = [[], []]
    limit = 9

    lastResult = None
    lastInput = [[], []]

    def __init__(self, name):
        self.name = name
        self.extractWeights()

    def recognize(self, input):
        sum = 0
        self.lastInput = input

        for i in range(len(input)):
            for j in range(len(input[i])):
                sum += input[i][j] * self.inputWeights[i][j]

        if sum >= self.limit:
            self.lastResult = True
            return sum/self.limit
        else:
            self.lastResult = False
            return sum / self.limit

    def punishNeuron(self):
        for i in range(len(self.inputWeights)):
            for j in range(len(self.inputWeights[i])):
                if self.lastResult is False:
                    self.inputWeights[i][j] += self.lastInput[i][j]
                else:
                    self.inputWeights[i][j] -= self.lastInput[i][j]
        self.saveWeights()


    def extractWeights(self):
        if self.matrixSaver.hasFile(self.name):
            self.inputWeights = self.matrixSaver.loadMtrixFromFile(self.name)
        else:
            self.inputWeights = self.createRaudomInputWeights()
            self.saveWeights()

    def saveWeights(self):
        self.matrixSaver.saveMatrixInFile(self.name, self.inputWeights)

    def createRaudomInputWeights(self):
        randomMatrix = [[0 for j in range(0, 32)] for i in range(0, 32)]
        for i in range(len(randomMatrix)):
            for j in range(len(randomMatrix[i])):
                randomMatrix[i][j] = random.randint(0, 1)

        return randomMatrix


