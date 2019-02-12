'''
Fichier principal
'''
from pyo import *
#from utils import ui 

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
#_server.amp = 0.1


_sineTest = Sine(freq=1000, phase=0, mul=1, add=0).out()

#_server.gui(locals())
