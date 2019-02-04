import serial, threading
from pyo import *

s = Server().boot().start()

a = Sine(1, [0, 0.25, 0.5, 0.75]).range(0, 1)
b = RCOsc(freq=[200,251,303,355], sharp=0.5, mul=a*0.3).out()

class SerialServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        # Change le port a ouvrir...
        self.serial = serial.Serial('/dev/ttyUSB0', 9600)

    def run(self):
        while 1:
            if self.serial.inWaiting() > 0:
                value = self.serial.readline()
                try:
                    # Assigne les valeurs lues aux frequences des lfos.
                    a.freq = int(value) * 0.005 + 1.0
                except:
                    pass
                # Dans cet exemple, les lfos sont utilises pour allumer des leds.
                amps = a.get(all=True)
                self.serial.write("1:" + str(int(amps[0]*128)) + "\n")
                self.serial.write("2:" + str(int(amps[1]*128)) + "\n")
                self.serial.write("3:" + str(int(amps[2]*128)) + "\n")
                self.serial.write("4:" + str(int(amps[3]*128)) + "\n")

server = SerialServer()
server.start()

s.gui(locals())
