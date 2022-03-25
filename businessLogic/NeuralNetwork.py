

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
        for neuron in self.neurons:
            if neuron.recognize(input):
                numberOfFiredNeurons += 1
                nameFiredNeuron = neuron.getName

        if numberOfFiredNeurons != 1:
            return False
        else:
            return nameFiredNeuron

    def getNeuronResult(self, neuronName, input):
        for neuron in self.neurons:
            if neuron.name == neuronName:
                self.trainableNeuron = neuron
                return neuron.recognize(input)

    def punishNeuron(self):
        self.trainableNeuron.punishNeuron()

