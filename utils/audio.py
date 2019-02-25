# encoding: latin-1
from pyo import *

#Si on veut rouler le fichier comme tel, enlever utils.
from utils.feuilles_v2 import VentFeuilles
from utils.pluie_V3 import PluieMateriaux
from utils.feu import Feu

#_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class Audio:
    def __init__(self):
        self._server = Server().boot()
        self._server.amp = 0.1
        
        #Test vent feuilles
        ventTest = VentFeuilles()
        ventTest.out()
        
        #Test feu
        #fire-all
        feuToFilter = Feu()
        feu01 = ButBP(feuToFilter.out(), freq=600, q=0.2, mul=0.5).mix(2).out() 
        feu02 = ButBP(feuToFilter.out(), freq=1200, q=0.6, mul=0.5).mix(2).out()
        feu03 = ButBP(feuToFilter.out(), freq=2600, q=0.4, mul=0.5).mix(2).out() 
        feu04 = Atone(feuToFilter.out(), freq=1000, mul=0.5).mix(2).out()
        
        #test pluie
        pluieMatTest = PluieMateriaux()

        #self.freqPort = SigTo(value=440, time=0.05, init=250)
        self.sineTest = Sine(freq=440, mul=0.3).mix(2).mix(2).out()

    def startServer(self, state):
        if state:
            self._server.start()
        else:
            self._server.stop()

    def setSineVolume(self, x):
        self.sineTest.mul = x
        
#audio = Audio()

#_server.gui(locals())
    