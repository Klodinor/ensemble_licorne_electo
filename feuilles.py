from pyo import *

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
_server.start()

def gust(x):
    """gust function"""
    noiseGust = Noise()
    lowpassGust01 = ButLP(noiseGust, freq=0.5)  
    lowpassGust02 = ButLP(lowpassGust01, freq=0.5)  
    highPass = ButHP(lowpassGust02, freq=0)
    highPass=highPass*50

    input = ((x + 0.5)*x)-0.125#--BUG--

    result = highPass * input
    return result
    
def squall(y):
    """squall"""
    input = (Max(y)-0.4)*8
    input = input*input
    
    noiseSquall = Noise()
    lpSquall01= ButLP(noiseSquall, freq=3)
    lpSquall02= ButLP(lpSquall01, freq=3)
    hpSquall = ButHP(lpSquall02, freq=0, mul=1, add=0)
    hpSquall = hpSquall * 20
    
    result = input * hpSquall
    return result

osc01 = Sine(freq=0.1, phase=0, mul=1, add=0)
osc01 = (osc01 + 1)*0.25

gustEtSquall = gust(osc01) + squall(osc01)

toClip = osc01 + gustEtSquall

toDelWrite = Clip(toClip, min=0, max=1)

delWrite = Delay1(toDelWrite, mul=1, add=0)
#SDelay(input, delay=0.25, maxdelay=1, mul=1, add=0) #Autre guess pour delaywrite


'''Algo 02'''
lowPass01 = ButLP(delWrite, freq=0.1)
lowPass01Math = ((lowPass01 * 0.4) + 0.3) - Sig(1)

noise01 = Noise()
noisemax = Max(noise01*lowPass01Math)#Comment faire cette opérations avec Max() 
noiseM = noisemax - lowPass01Math
noiseF = noiseM * lowPass01Math

hp01 = ButHP(noiseF, freq=200, mul=1, add=0)
lowPass02 = ButLP(hp01, freq=4000, mul=1, add=0)

lpCombined = (lowPass02 * lowPass01)*1.2
#lpCombined.mix(2).out()#Pourquoi ne marche pas en mix(2)
lpCombined.out()

_server.gui(locals())
