# encoding: latin-1
from pyo import *
import math # pour PI

#_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class PluieMateriaux:
    """Pluie sur matériaux solide"""
    def __init__(self):
        self.gaussianNoise_01 = self.gaussianNoise(0.4)

        self.bp01 = ButBP(self.gaussianNoise_01, freq=50, q=0.4) # bp~ est aussi de second ordre.

        self.lp01 = Tone(self.bp01, freq=500)

        self.lp02 = (self.lp01 * 80) + 40
        self.phasor01 = Phasor(freq=self.lp02, add=-0.25)
        self.cos01 = Cos(self.phasor01*math.pi*2) # L'objet cos~ de puredata effectue la multiplication par 2pi à l'interne.

        self.total = self.cos01 * ((self.lp01 ** 2) * 10)

        # Le seuil ici est important (en passant de 0.35 à 0.05, on s'approche de quelque chose)
        # Plus il est petit, plus on entend de granules, plus haut que 0.1, c'est le silence...
        self.maxTotal = Max(self.total, comp=0.05, add=-0.05) 

        self.totalToFilter = self.maxTotal

        self.hp01 = Atone(self.totalToFilter, freq=500)
        self.hp02 = Atone(self.hp01, freq=500)#.out()
        
    def gaussianNoise(self, amount=0.4):
        self.noiseGaus01 = Noise()
        self.max = Max(self.noiseGaus01, comp=0)
        self.min = Min(self.noiseGaus01, comp=0) * -1
        self.minMaxTotal = self.max + self.min
        self.sig01 = Sig(amount)
        self.sig02 = Sig(1) - self.sig01
        self.totalMath = (Log((self.minMaxTotal*self.sig01)+self.sig02))*-2
        self.squareRoot = Sqrt(self.totalMath)
        self.noiseGaus02 = Cos(Noise(mul=2*math.pi)) # L'objet cos~ de puredata effectue la multiplication par 2pi à l'interne. 
        self.output = self.squareRoot*self.noiseGaus02 # self.output est ton gaussian noise.
        return self.output
        
    def volume(self, x):
        self.hp02.mul = x


    def out(self):
        output = self.hp02.out()
        return output



#pluieMatTest = PluieMateriaux()
#pluieMatTest.out()

#_server.gui(locals())
