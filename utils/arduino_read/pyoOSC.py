from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

def pp(address, *args):
    #print(address)
    print(args)

#Quand je recois de l'osc j'execute la fonction pp
r = OscDataReceive(9900, "/imu", pp)
#utiliser dataReceive dans une fonction qui update des sig qui gère mes instruments audio.

'''
#Pour le receive - Quel dois-je utiliser?
a = OscListReceive(port=10001, address=['/pitch', '/amp'], num=8)
b = Sine(freq=a['/pitch'], mul=a['/amp']).mix(2).out()

a = OscReceive(port=10001, address=['/pitch', '/amp'])
b = Sine(freq=a['/pitch'], mul=a['/amp']).mix(2).out()


#Pour le send - Quel dois-je utiliser?
a = OscDataSend("fissif", 9900, "/data/test")
msg = [3.14159, 1, "Hello", "world!", 2, 6.18]
a.send(msg)

a = Sine(freq=[1,1.5], mul=[100,.1], add=[600, .1])
b = OscSend(a, port=10001, address=['/pitch','/amp'])
'''

s.gui(locals())
