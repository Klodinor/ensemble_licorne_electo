# encoding: latin-1
from pyo import *
import math

#Si on veut rouler le fichier comme tel, enlever utils.
from utils.feuilles_v2 import VentFeuilles
from utils.pluie_V3 import PluieMateriaux
from utils.feu import Feu
from utils.fatbass import FatBass

class Audio:
    def __init__(self):
        self._server = Server().boot()
        #self._server.amp = 0.1

        #Quand je recois de l'osc j'execute la fonction pp
        self.OSCReceive = OscDataReceive(9900, "/imu", self.dataReceive)

        #Variable globale qui store le volume courant des instruments
        #self.volumeCourant = Sig(0)

        #Var global son actuel dry
        self.dry = Sig(0)

        '''Bloc Initialisation Instruments'''
        #self.freqPort = SigTo(value=440, time=0.05, init=250)
        #self.sineTest = Sine(freq=440, mul=0.3).mix(2).mix(2).out()
        
        #Feuilles
        self.ventTest = VentFeuilles()
        
        #Pluie Mat
        self.pluieMatTest = PluieMateriaux()
        
        #Feu
        self.feuToFilter = Feu()
        self.feu01 = ButBP(self.feuToFilter.out(), freq=600, q=0.2, mul=0.5)
        self.feu02 = ButBP(self.feuToFilter.out(), freq=1200, q=0.6, mul=0.5)
        self.feu03 = ButBP(self.feuToFilter.out(), freq=2600, q=0.4, mul=0.5)
        self.feu04 = Atone(self.feuToFilter.out(), freq=1000, mul=0.5).mix(2)

        #FatBass
        self.octave = Sine([0.15,0.13]).range(0.1, 0.9)
        self.duty = Sine([0.07, .1]).range(0.1, 0.5)
        self.fatbass = FatBass(80, self.octave, self.duty, 2500, 0, mul=0.4)#.out()
        #self.fatbass.ctrl()
        '''FIN Bloc Initialisation Instruments'''

        '''Bloc Initialisation Effets'''
        #Disto
        self.disto01 = Disto(self.dry, drive=0.85, slope=0.35, mul=1)
        #Reverb Stereo
        self.reverb01 = STRev(self.dry, inpos=0.5, revtime=23.5, cutoff=3550, bal=0.5, roomSize=4, firstRefGain=-3, mul=1)
        #delai Stereo
        self.delai01 = Delay(self.dry, delay=3, feedback=0.5, maxdelay=15, mul=1)
        
        #C'est dans cette var que les effets et le dry son entreposes
        self.outputEffetsVoice = Sig(0)
        self.outputEffets = Selector([self.dry, self.disto01, self.reverb01, self.delai01], voice=self.outputEffetsVoice, mul=1, add=0)
        '''FIN Bloc Initialisation Effets'''
        
    def dataReceive(self, address, *args):
        #print(address)
        #print(args)
        
        #Convertion des donnees recu en radian en degree
        self.yawAxisInDeg = math.degrees(args[0])
        self.pitchAxisInDeg = math.degrees(args[1])
        self.rollAxisInDeg = math.degrees(args[2])
        
        #Action sur l'audio
        #JE DOIS ENVOYER dans outputEffetsVoice --> self.yawAxisInDeg mapper entre 0 & 1
        #self.outputEffetsVoice.value = self.yawAxisInDeg
        #print(self.outputEffetsVoice.value)
        '''if self.yawAxisInDeg <= 45:
            self.outputEffetsVoice.value = 0
            print(45)
        elif self.yawAxisInDeg <= 90:
            self.outputEffetsVoice.value = 1
            print(90)
        elif self.yawAxisInDeg <= 135:
            self.outputEffetsVoice.value = 2
            print(135)
        elif self.yawAxisInDeg <= 180:
            self.outputEffetsVoice.value = 3
            print(180)'''
            
        #Remplacer outmin et outmax par la valeur total de 'voice' de mon selector. Donc le .lenght() de mon array avec les effets.
        #faire en sorte que si les donnees sont dans le negatif, de le mettre en positif.
        scaleSig = Scale(Sig(self.yawAxisInDeg), inmin=-180, inmax=180, outmin=-1, outmax=1, exp=1, mul=1, add=0)#recoit des obj audio
        scale = rescale(*args, **kwargs)#donnees uniquement    


    def startServer(self, state):
        if state:
            self._server.start()
        else:
            self._server.stop()
        
    def setVolume(self, vol):
        '''Verifi si l'instrument joue, si oui ajuste le volume'''
        #self.sineTest.mul = x
        #print(vol)        

        #variable globale du volume
        #self.volumeCourant.value = vol
        
        #if self.ventTest.isOut() == True:
        #feuilles
        self.ventTest.volume(vol)
        #elif self.pluieMatTest.isOut()== True:
        #pluie
        self.pluieMatTest.volume(vol*20)
        #elif self.feu01.isOutputting() == True:
        #feu
        self.feu01.mul = vol/20
        self.feu02.mul = vol/20
        self.feu03.mul = vol/20
        self.feu04.mul = vol/20
        #FatBass
        self.fatbass.mul = vol/2
        
    def setInstrument(self, x):
        #On veut activer l'instrument en question ET mute les autres
        if x==0:
            #Vent feuilles
            self.closeInst('vent_feuilles')
            #self.ventTest.out()
            self.dry = self.ventTest
            self.dry.out()
            #self.ventTest.volume = self.volumeCourant
        elif x==1:
            #Pluie Materiaux
            self.closeInst('pluie_materiaux')
            #self.pluieMatTest.out()
            self.dry = self.pluieMatTest
            self.dry.out()
            #self.pluieMatTest.volume = volumeCourant
        elif x==2:
            self.closeInst('feu')
            #Feu
            #fire-all
            self.feu01.out()#.mix(2).out() 
            self.feu02.out(1)#.mix(2).out()
            self.feu03.out()#.mix(2).out() 
            self.feu04.out(1)#.mix(2).out(1)
            #mettre au volume actuel du slider
            #self.feu01.mul = volumeCourant
            #self.feu02.mul = vvolumeCourant
            #self.feu03.mul = volumeCourant
            #self.feu04.mul = volumeCourant
        elif x==3:
            #Aller chercher l'instrument Fat Bass du prof et modifier
            self.closeInst('fatbass')
            self.dry= self.fatbass
            self.dry.out()
            #self.fatbass.mul = volumeCourant
            
    def closeInst(self, currInst):
        """ferme tout les instruments qui ne sont pas celui passe en attribut"""
        if currInst == 'vent_feuilles':
            #Stop pluie
            self.pluieMatTest.stop()
            #stop Feu
            self.feu01.stop()
            self.feu02.stop()
            self.feu03.stop()
            self.feu04.stop()
            #stop bass
            self.fatbass.stop()
            
        elif currInst == 'pluie_materiaux':
            #Stop feuilles
            self.ventTest.stop()
            #stop Feu
            self.feu01.stop()
            self.feu02.stop()
            self.feu03.stop()
            self.feu04.stop()
            #stop bass
            self.fatbass.stop()
            
        elif currInst == 'feu':
            #Stop feuilles
            self.ventTest.stop()
            #stop bass
            self.fatbass.stop()
            #Stop pluie
            self.pluieMatTest.stop()
            
        elif currInst == 'fatbass':
            #Stop feuilles
            self.ventTest.stop()
            #stop Feu
            self.feu01.stop()
            self.feu02.stop()
            self.feu03.stop()
            self.feu04.stop()
            #Stop pluie
            self.pluieMatTest.stop()
        
        elif currInst == 'all':
            #Stop feuilles
            self.ventTest.stop()
            #stop Feu
            self.feu01.stop()
            self.feu02.stop()
            self.feu03.stop()
            self.feu04.stop()
            #Stop pluie
            self.pluieMatTest.stop()
            #stop bass
            self.fatbass.stop()

    def effets(self, isOn):
        """Gestion des effets"""
        if isOn == 1:
            print('on')
            self.closeInst('all')
            self.disto01.input = self.reverb01.input = self.delai01.input = self.dry.out()
            self.outputEffets.input = [self.dry, self.disto01, self.reverb01, self.delai01]
            self.outputEffets.out()
            self.outputEffets.voice = 1
        else:
            print('off')
            self.dry.out()
            self.outputEffets.stop()
            


 
'''
LOGIQUE Pour l'utlilisation des effets  :

le son qui est ouput par mon set instrument et stock dans la var dry (qui est un input fader)

quand j'active le on/off du bouton, ce n'est plus mon instruments qui envoi du son mais la var outpu ce dessous, où voice = interpolation entre tout mes effets et le dry wet 

''' 
#dry = InputFader(input)#setInput feu, vent ou autre
#output = Selector([dry, disto, reverb, delai], voice=0.00, mul=1, add=0)#voice fonctionne +1 par agument pour la valeur totale de voice

if __name__ == '__main__':
    _server = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
    audio = Audio()
    _server.gui(locals())
    