from pyo import *

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
_server.amp=0.1

def gaussianoise(amount):
    """Bruit gossien"""
    noiseGaus01 = Noise()
    max = Max(noiseGaus01, comp=0)
    min = Min(noiseGaus01, comp=0) * -1
    
    minMaxTotal = max+min
    
    sig01 = Sig(amount)
    sig02 = Sig(1) - sig01

    totalMath = (Log((minMaxTotal*sig01)+sig02))*-2
    
    squareRoot = Sqrt(totalMath)
    
    noiseGaus02 = Cos(Noise())
    
    output = squareRoot*noiseGaus02
    
    return output


gaussianNoise_01 = gaussianoise(0.4)

bp01 = ButBP(gaussianNoise_01, freq=50, q=0.2)#j'ai mis le Q à 0.2 et non 0.4, car il s'agit d'un filtre de second et non de premier ordre.

lp01 = Tone(bp01, freq=500)

lp01 =(lp01*80)+40

phasor01 = Phasor(freq=lp01)

phasor01 = phasor01-0.25

cos01 = Cos(phasor01)


total = cos01 * ((lp01**2)*10)
maxTotal = Max(total, comp=0.35)

totalToFilter = (maxTotal - 0.35)*0.5

hp01 = Atone(totalToFilter, freq=500)
hp02 = Atone(hp01, freq=500).out()

_server.gui(locals())
