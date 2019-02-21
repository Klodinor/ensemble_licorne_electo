#!/usr/bin/env python3
# encoding: mbcs

from pyo import *
import math
import wx

#mes imports
app = wx.App()
from utils import ui


_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
#_server.amp = 0.1

sineTest = Sine(freq=440).mix(2).out()




app.MainLoop()
#_server.gui(locals())
