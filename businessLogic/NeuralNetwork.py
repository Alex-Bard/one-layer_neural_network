from businessLogic.Neuron import Neuron

class NeuralNetwork(object):
    neurons = []
    trainableNeuron = None

    def __init__(self, neuronNamesList):
        for name in neuronNamesList:
            self.neurons.append(Neuron(name))

    def recognize(self, input):
        # to prevent learning of another neuron
        self.trainableNeuron = None


        numberOfFiredNeurons = 0
        nameFiredNeuron = ""
        coefFiredNeuron = 0
        for neuron in self.neurons:
            coef = neuron.recognize(input)
            if coef >= 1:
                numberOfFiredNeurons += 1
                nameFiredNeuron = neuron.name
                coefFiredNeuron = coef

        if numberOfFiredNeurons != 1:
            return False, 0
        else:
            return nameFiredNeuron, coefFiredNeuron

    def getNeuronResult(self, neuronName, input):
        for neuron in self.neurons:
            if neuron.name == neuronName:
                self.trainableNeuron = neuron
                return neuron.recognize(input)

    def punishNeuron(self):
        self.trainableNeuron.punishNeuron()

