from pyo import *
import random

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

class Feu:
    """Feu"""
    def __init__(self):
        self.noise01 = Noise()
        #modifier aussi ces valeurs avec donnees capteur?
        self.crackling = self.crackling(self.noise01)*0.2
        self.hissing01 = self.hissing(self.noise01)*0.3
        self.lapping01 = self.lapping(self.noise01)*0.6
        
    def hissing(self, noise):
        #self.noise01 = Noise()
        self.noise01 = noise
        self.hp01 = Atone(self.noise01, freq=1000)
        self.lp01 = Tone(self.noise01, freq=1)
        self.lpMath = (((self.lp01*10)**2)**2)*600
        self.total = self.hp01 * self.lpMath
        return self.total
        
    def crackling(self, noise):
        #self.noise01 = Noise()
        self.noise01 = noise
        self.lop01 = Tone(self.noise01, freq=1)
        
        #cutoff highpass? analyse tout le spectre?
        self.follow01 = Follower(self.lop01, freq=20)
        
        self.random01 = 2000
        if self.follow01 >= 50 and self.follow01 < 51:
            self.random01 = random.randint(0,28)
            
        #line~ en pyhton?
        self.line = 1+self.random01#To change
        self.lineMath = ((self.line**2)**2)


        self.randomMath = (self.random01*500)+1500
        self.bp01 = ButBP(self.noise01, freq=self.random01, q=1)
        
        self.total = self.lineMath * self.bp01
        return self.total
        
    def lapping(self, noise):
        #self.noise01 = Noise()
        self.noise01 = noise
        self.bp01 = ButBP(self.noise01, freq=30, q=5)
        self.bpMath =  self.bp01*100
        self.hp01 = Atone(self.bpMath, freq=25)
        self.clip01 = Clip(self.hp01, min=-0.9, max=0.9)
        self.hp02 = Atone(self.clip01, freq=25)
        self.total = self.hp02*0.6
        
        return self.total

#fire-all
feu01 = ButBP(Feu(), freq=600, q=0.2) 
feu02 = ButBP(Feu(), freq=1200, q=0.6) 
feu03 = ButBP(Feu(), freq=2600, q=0.4) 
feu04 = Atone(Feu(), freq=1000)




_server.gui(locals())
