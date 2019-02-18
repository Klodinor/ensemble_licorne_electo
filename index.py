# encoding: mbcs
'''
Fichier principal
'''
from pyo import *
import math
from utils import ui 
import wx

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
#_server.amp = 0.1


_sineTest = Sine(freq=1000, phase=0, mul=1, add=0).out()

app = wx.App()
#app.Maximize(True)
frm = mainFrame(None, title='Ensemble Accéléromètre Électro')
frm.Show()
app.MainLoop()

#_server.gui(locals())
