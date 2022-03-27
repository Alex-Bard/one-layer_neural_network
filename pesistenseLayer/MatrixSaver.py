from os.path import exists
import pickle

class MatrixSaver(object):

    def getFilePuthToNeuronWeights(self,neuronName):
        puth = "neuronWeights/" + neuronName + ".data"
        return puth

    def hasFile(self, neuronName):
        return exists(self.getFilePuthToNeuronWeights(neuronName))

    def loadMtrixFromFile(self, neuronName):
        with open(self.getFilePuthToNeuronWeights(neuronName), "rb") as f:
            return pickle.load(f)

    def saveMatrixInFile(self, neuronName, matrix):
        with open(self.getFilePuthToNeuronWeights(neuronName), 'wb') as f:
            pickle.dump(matrix, f)

    def savePicture(self, filePuth, matrix):
        with open(filePuth, 'wb') as f:
            pickle.dump(matrix, f)
        return True

    def checkFile(self, filePuth):
        return exists(filePuth)

    def loadPicture(self, filePuth):
        with open(filePuth, 'rb') as f:
            return pickle.load(f)
