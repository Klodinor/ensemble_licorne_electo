from pyo import *

_server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()




_server.gui(locals())
