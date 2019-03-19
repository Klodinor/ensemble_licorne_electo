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
        #self._server.amp = 0.1

        #self.freqPort = SigTo(value=440, time=0.05, init=250)
        #self.sineTest = Sine(freq=440, mul=0.3).mix(2).mix(2).out()
        #Feuilles
        self.ventTest = VentFeuilles()
        #Pluie Mat
        self.pluieMatTest = PluieMateriaux()
        #Feu
        self.feuToFilter = Feu()
        

    def startServer(self, state):
        if state:
            self._server.start()
        else:
            self._server.stop()
        
    def setVolume(self, x):
        #self.sineTest.mul = x
        #faire baisser le volume de tout les instruments indépendemment de si ils joue en ce moment ou non
        #feuilles
        self.ventTest.volume(x)
        #pluie
        self.pluieMatTest.volume(x)
        
    def setInstrument(self, x):
        #On veut activer l'instrument en question ET mute les autres
        if x==0:
            #Vent feuilles
            self.ventTest.out()
        elif x==1:
            #Pluie Materiaux
            self.pluieMatTest.out()
        elif x==2:
            #Feu
            #fire-all
            feu01 = ButBP(self.feuToFilter.out(), freq=600, q=0.2, mul=0.5).mix(2).out() 
            feu02 = ButBP(self.feuToFilter.out(), freq=1200, q=0.6, mul=0.5).mix(2).out()
            feu03 = ButBP(self.feuToFilter.out(), freq=2600, q=0.4, mul=0.5).mix(2).out() 
            feu04 = Atone(self.feuToFilter.out(), freq=1000, mul=0.5).mix(2).out()
        elif x==3:
            #Aller chercher l'instrument Fat Bass du prof et modifier
            print('Instru 04');
        else:
            #faire jouer l'instrument un si whatever
            print('Bug');
            

#audio = Audio()

#_server.gui(locals())
    