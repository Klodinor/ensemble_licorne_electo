from pyo import *
import serial

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
_server.start()

def gust(x):
    """gust function"""
    noiseGust = Noise()
    lowpassGust01 = Tone(noiseGust, freq=0.5)  
    lowpassGust02 = Tone(lowpassGust01, freq=0.5)  
    highPass = Atone(lowpassGust02, freq=0)
    highPass=highPass*50

    #input = ((x + 0.5)*x)-0.125#--BUG--
    input = x + 0.5
    inputexp = (input**2)-0.125

    result = highPass * inputexp
    return result
    
def squall(y):
    """squall"""
    input = (Max(y)-0.4)*8
    input = input**2
    
    noiseSquall = Noise()
    lpSquall01= Tone(noiseSquall, freq=3)
    lpSquall02= Tone(lpSquall01, freq=3)
    hpSquall = Atone(lpSquall02, freq=0, mul=1, add=0)
    hpSquall = hpSquall * 20
    
    result = input * hpSquall
    return result

osc01 = Sine(freq=0.1, phase=0, mul=1, add=0)
osc01 = (osc01 + 1)*0.25

gustEtSquall = gust(osc01) + squall(osc01)

toClip = osc01 + gustEtSquall

toDelWrite = Clip(toClip, min=0, max=1)

delWrite = Delay(toDelWrite, delay=2, feedback=0, maxdelay=2, mul=1, add=0)


'''Algo 02'''
lowPass01 = Tone(delWrite, freq=0.1)
lowPass01Math = Sig(1) - ((lowPass01 * 0.4) + 0.3)

noise01 = Noise()
#noisemax = Max(noise01*lowPass01Math)#Comment faire cette opérations avec Max() 
noisemax = Max(noise01, comp=lowPass01Math, mul=1, add=0)
noiseM = noisemax - lowPass01Math
noiseF = noiseM * lowPass01Math

hp01 = Atone(noiseF, freq=200, mul=1, add=0)
lowPass02 = Tone(hp01, freq=4000, mul=1, add=0)

lpCombined = ((lowPass02 * lowPass01)*1.2).mix(2)
lpCombined.out()

_server.gui(locals())
