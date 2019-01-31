from pyo import *

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

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

bp01 = ButBP(gaussianNoise_01, freq=50, q=0.2, mul=1, add=0)#j'ai mis le Q à 0.2 et non 0.4, car il s'agit d'un filtre de second et non de premier ordre.

lp01 = Tone(bp01, freq=500)


_server.gui(locals())
