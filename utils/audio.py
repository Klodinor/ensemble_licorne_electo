# encoding: latin-1
from pyo import *

from utils.feuilles_v2 import VentFeuilles
from utils.pluie_V3 import PluieMateriaux
from utils.feu import Feu

class Audio:
    def __init__(self):
        self._server = Server().boot()
        self._server.amp = 0.1
        
        #self.freqPort = SigTo(value=440, time=0.05, init=250)
        self.sineTest = Sine(freq=440, mul=0.3).mix(2).mix(2).out()

    def startServer(self, state):
        if state:
            self._server.start()
        else:
            self._server.stop()

    def setSineVolume(self, x):
        self.sineTest.mul = x
