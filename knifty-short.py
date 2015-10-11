import random as rand
from itertools import izip

class Neuron(object):
    _ACTIV = 1
    _INACTIV = 0
    _delta = [[2,-2],[-8,10]] #hebbian adjustment matrix
    _dThresh = 1 #value of threshold adjustment

    def __init__(self):
        self.thresh = 2**16 -1
        self.activ = self._INACTIV
        self.inNodes = []
        self.outNodes = []
        self.inWeights = [] #not making this a dict could be a mistake
        self.stimulus = 0
        self.cyclesSinceFiring = 0

    def activate(self,adjustWts=True):
        accu = 0
        accu += self.stimulus
        for node,weight in izip(self.inNodes,self.inWeights): accu += node.activ * weight
        self.activ = self._ACTIV if (accu > self.thresh) else self._INACTIV
        if adjustWts: self.hebbify()

    def hebbify(self):
        n = 1 if (self.activ > 0) else 0
        for node,weight in izip(self.inNodes,self.inWeights):
            x = 1 if (node.activ > 0) else 0
            weight += self._delta[n][x]
        if n:
            self.cyclesSinceFiring = 0
            self.thresh += self._dThresh
        else:
            self.cyclesSinceFiring += 1
            self.thresh -= self._dThresh * self.cyclesSinceFiring

    def init_weights(self):
        self.inWeights = [rand.randint(-65535,65535) for node in self.inNodes]

class Layer(object):
    def __init__(self,n_nodes=3,neuron_class=Neuron):
        self._neuron_class = neuron_class
        self.make_nodes(n_nodes)
        self.outLayers = []
        self.output = []

    def stimulate(self,stimVector):
        if not (len(stimVector) == len(self.nodes)): raise Exception( "Stimulus vector length error")
        else:
            for node,stimulus in izip(self.nodes,stimVector):
                node.stimulus = stimulus
            self.propagate()

    def propagate(self):
        for node in self.nodes: node.activate()
        for layer in self.outLayers: layer.propagate()
        if len(self.outLayers) == 0:
            self.output = self.get_activ_state()

    def get_activ_state(self): return [node.activ for node in self.nodes]

    def make_nodes(self,n_nodes):
        self.nodes = [self._neuron_class() for i in xrange(n_nodes)]

    def connect_inLayer(self,inLayer):
        inLayer.connect_outLayer(self) #connect back
        for node in self.nodes:
            node.inNodes = inLayer.nodes
            node.init_weights()

    def connect_outLayer(self,outLayer): self.outLayers.append(outLayer)

class Net(object):
    def __init__(self,sizeTuple,layer_class=Layer):
        self._layer_class = layer_class
        self.layers = []
        self.make_layers(sizeTuple)

    def make_layers(self,sizeTuple):
        for sz in sizeTuple:
            self.layers.append(self._layer_class(sz))
        for i,layer in enumerate(self.layers[1:],1):
            layer.connect_inLayer(self.layers[i-1])

    def stimulate(self,stimVector): self.layers[0].stimulate(stimVector)

    def get_activ_state(self): return self.layers[-1].get_activ_state()
