from pyo import *
import math # pour PI

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class GaussianNoise:
    def __init__(self, amount=0.4):
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

gaussianNoise_01 = GaussianNoise(0.4)

bp01 = ButBP(gaussianNoise_01.output, freq=50, q=0.4) # bp~ est aussi de second ordre.

lp01 = Tone(bp01, freq=500)

lp02 = (lp01 * 80) + 40
phasor01 = Phasor(freq=lp02, add=-0.25)
cos01 = Cos(phasor01*math.pi*2) # L'objet cos~ de puredata effectue la multiplication par 2pi à l'interne.

total = cos01 * ((lp01 ** 2) * 10)

# Le seuil ici est important (en passant de 0.35 à 0.05, on s'approche de quelque chose)
# Plus il est petit, plus on entend de granules, plus haut que 0.1, c'est le silence...
maxTotal = Max(total, comp=0.05, add=-0.05) 

totalToFilter = maxTotal

hp01 = Atone(totalToFilter, freq=500)
hp02 = Atone(hp01, freq=500).out()

_server.gui(locals())
