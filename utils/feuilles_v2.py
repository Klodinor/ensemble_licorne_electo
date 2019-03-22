# encoding: latin-1
from pyo import *

#_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
#_server.start()

class VentFeuilles:
    """Vent dans feuilles class intruments"""
    def __init__(self):
        self.osc01 = Sine(freq=0.1, phase=0, mul=1, add=0)
        self.osc02 = (self.osc01 + 1)*0.25

        self.gustEtSquall = self.gust(self.osc02) + self.squall(self.osc02)

        self.toClip = self.osc02 + self.gustEtSquall

        self.toDelWrite = Clip(self.toClip, min=0, max=1)

        self.delWrite = Delay(self.toDelWrite, delay=2, feedback=0, maxdelay=2, mul=1, add=0)

        '''Algo 02'''
        self.lowPass01 = Tone(self.delWrite, freq=0.1)
        self.lowPass01Math = Sig(1) - ((self.lowPass01 * 0.4) + 0.3)

        self.noise01 = Noise()
        self.noisemax = Max(self.noise01, comp=self.lowPass01Math, mul=1, add=0)
        self.noiseM = self.noisemax - self.lowPass01Math
        self.noiseF = self.noiseM * self.lowPass01Math

        self.hp01 = Atone(self.noiseF, freq=200, mul=1, add=0)
        self.lowPass02 = Tone(self.hp01, freq=4000, mul=1, add=0)

        self.lpCombined = ((self.lowPass02 * self.lowPass01)*1.2).mix(2)
        #self.lpCombined.out() -- remplacer par def out()
        
    def gust(self, x):
        """gust function"""
        self.x = x    

        self.noiseGust = Noise()
        self.lowpassGust01 = Tone(self.noiseGust, freq=0.5)  
        self.lowpassGust02 = Tone(self.lowpassGust01, freq=0.5)  
        self.highPass = Atone(self.lowpassGust02, freq=0)
        self.highPass=self.highPass * 50

        #input = ((x + 0.5)*x)-0.125#--BUG--
        self.input = self.x + 0.5
        self.inputexp = (self.input**2)-0.125

        self.result = self.highPass * self.inputexp
        return self.result
    
    def squall(self, y):
        """squall"""
        self.y = y    

        self.input_01 = (Max(self.y)-0.4)*8
        self.input_02 = self.input_01**2
        
        self.noiseSquall = Noise()
        self.lpSquall01= Tone(self.noiseSquall, freq=3)
        self.lpSquall02= Tone(self.lpSquall01, freq=3)
        self.hpSquall = Atone(self.lpSquall02, freq=0, mul=1, add=0)
        self.hpSquall = self.hpSquall * 20
        
        self.result = self.input_02 * self.hpSquall
        return self.result
    
    def volume(self, vol):
        self.lpCombined.mul = vol
        #OU FAIRE SUR 
        #self.hp01.mul
        #self.lowPass02.mul
        
    def isOut(self):
        if self.lpCombined.isOutputting() == True:
            return True

    def out(self, chnl=0):
        output = self.lpCombined.out()
        return output
        
    def stop(self):
        self.lpCombined.stop()
        
        

#ventTest = VentFeuilles()
#ventTest.out()


#_server.gui(locals())
