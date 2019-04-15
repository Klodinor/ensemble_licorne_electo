# encoding: latin-1
import wx
from pyo import *
from utils.audio import Audio


class MainFrame(wx.Frame):
    """
    Interface utilisateur principal
    """
    def __init__(self, audio=None, title=''):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(None, title=title)
        
        #Met l'interface en full screen
        self.Maximize()
        
        # create a panel in the frame - Panel s'insere dans le frame et permet de placer des elemets dessus
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundColour("#777777")#set la couleur du panel

        #On creer la var qui represente l'audio - BUG
        self.audio = audio

        # and put some text with a larger bold font on it --> st = string, gere ce qui a trait au texte lui meme & font, tout ce qui a trait a la police de caractere 
        self.st = wx.StaticText(self.pnl, label="Ensemble Accéléromètre Électro", pos=(5,5))
        self.st.SetForegroundColour("#ffffff")
        self.font = self.st.GetFont()
        self.font.PointSize += 5
        #font = font.Bold()
        self.st.SetFont(self.font)

        # create a menu bar
        self.makeMenuBar()
        
        """Gestion Acticvation du serveur Audio"""
        self.onOffText = wx.StaticText(self.pnl, id=-1, label="Audio",
                                       pos=(28,30), size=wx.DefaultSize)
        self.onOff = wx.ToggleButton(self.pnl, id=-1, label="on / off",
                                     pos=(10,48), size=wx.DefaultSize)
        # Un event du toggle appelle la methode self.handleAudio
        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)
        """Gestion Acticvation du serveur Audio"""
        
        """Gestion Calibration"""
        self.onOffText = wx.StaticText(self.pnl, id=-1, label="Étalonnage",
                                       pos=(28,80), size=wx.DefaultSize)
        self.onOff = wx.ToggleButton(self.pnl, id=-1, label="Fait!",
                                     pos=(10,98), size=wx.DefaultSize)
        # Un event du toggle appelle la methode self.handleAudio
        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.handleCalibration)
        """Fin gestion calibration"""

        '''Init des slider, btn & dropdown de mon interface -- provient des notes d'Olivier Belanger'''
        ############# Initialise la premiere barre d'effet pour l'instrumentiste 01#############
        self.onOffText_effet01 = wx.StaticText(self.pnl, id=-1, label="Inst_01 effets", 
                                       pos=(610, 60), size=wx.DefaultSize)
        self.onOff_effet01 = wx.ToggleButton(self.pnl, id=-1, label="On/Off", 
                                     pos=(608, 80), size=wx.DefaultSize)
        # Un event du toggle appelle la methode self.handleAudio
        self.onOff_effet01.Bind(wx.EVT_TOGGLEBUTTON, self.gestionEffets)

        # Liste de son contenus dans le meme dossier que le script
        '''effets = ['Delai', 'Disto', 'Reverb', 'Harmonizer']
        self.popupText = wx.StaticText(self.pnl, id=-1, 
                                       label="Choisir un effet",
                                       pos=(10, 130), size=wx.DefaultSize)
        self.popup = wx.Choice(self.pnl, id=-1, pos=(8, 145), 
                               size=(150, -1), choices=effets)
        self.popup.SetSelection(0)'''
        ############# FIN initialise la premiere barre d'effet pour l'instrumentiste 01#############    
        

        
        instType = ['Vent Feuilles', 'Pluie', 'Feu', 'Synth Bass']
        self.popupText_ints01 = wx.StaticText(self.pnl, id=-1, 
                                       label="Choisir un instrument",
                                       pos=(610, 10), size=wx.DefaultSize)
        self.popup_ints01 = wx.Choice(self.pnl, id=-1, pos=(605, 30), 
                               size=(150, -1), choices=instType)
        self.popup_ints01.SetSelection(0)
        self.popup_ints01.Bind(wx.EVT_CHOICE, self.changeInst)
        
        #Label Slider volume instrument 01
        self.volInst01 = wx.StaticText(self.pnl, id=-1, label="Inst_01 Volume", pos=(610, 115), size=wx.DefaultSize)
        #Slider volume instrument 01
        self.volInst01 = wx.Slider(self.pnl, style=wx.SL_VERTICAL|wx.SL_INVERSE|wx.SL_LABELS, id=1, value=0, minValue=-60, maxValue=18, pos=(605, 127), size=(-1, 250))#Ou 0 = 0 & 100 = 1
        #fonction de callBack a defenir
        self.volInst01.Bind(wx.EVT_SLIDER, self.changeVolume)
        ''' FIN Init des slider, btn & dropdown de mon interface -- provient des notes d'Olivier Belanger'''

        # and a status bar -- un footer 
        #self.CreateStatusBar()
        #self.SetStatusText("Main User interface")
        
    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        ''' Fait la création de l'onglet file --> wx.menu & creer ces deux sous-menu 'hello' et 'exit '''
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers --> bref gestiond des 'shortcut'
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H", "Cette phrase apparaît au bas de l'ecran")
        #Le separateur par defaut des menu standart, purement visuel
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        exitItem = fileMenu.Append(wx.ID_EXIT)



        '''Fait la creation de l'onglet help'''
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        '''Creer la barre de menu elle-meme et y ajoute/append les deux menu cree ci-haut --> le "&Nom" = le nom du menu en question '''
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    '''
    def createFreqSlider(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, -1, "Volume Instrument 1")
        sizer.Add(label, 0, wx.CENTER|wx.ALL, 5)
        self.freq = PyoGuiControlSlider(parent=self.panel,
                                        minvalue=20,
                                        maxvalue=20000,
                                        init=1000,
                                        pos=(0, 0),
                                        size=(200, 16),
                                        log=True,
                                        integer=False,
                                        powoftwo=False,
                                        orient=wx.HORIZONTAL)
        #print(self.freq.getRange())
        #print(self.freq.isPowOfTwo())
        self.freq.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeFreq)
        sizer.Add(self.freq, 0, wx.ALL | wx.EXPAND, 5)
        return sizer
        '''
        
    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)
    #Gestion activation de l'audio
    def handleAudio(self, evt):
        self.audio.startServer(evt.GetInt())
        
    def handleCalibration(self, evt):
        """Call calibraiton fonction"""
        self.audio.doCalibration()

    def gestionEffets(self, evt):
        self.audio.effets(evt.GetInt())
        
    def changeVolume(self, evt):
        if isinstance(evt, float):
            x = 10**(evt/20)
            self.audio.setVolume(x)
        else:
            #formuleConvertionDb
            x = 10**(evt.GetInt()/20)
            self.audio.setVolume(x)

        #x = evt.GetInt() / 100 -->vieux volume

        #self.volInst01.SetLabel("Volume : %.3f" % x)
        #sineTest.mul = x
        
    def changeInst(self, evt):
        x = evt.GetInt()
        #Activer une classe de l'instrument en question
        self.audio.setInstrument(x)
        
    def midiVolumeChange(self, x):
        """Doc string for fname function."""
        self.volInst01.SetValue(x)
        

#POUR GERER mes 10 voix, passer une liste [Audio(), Audio(), etc] et les apellers avec audio[x] dans MainFrame()
_audio = Audio()

'''Gestion Voume MIDI'''
def event(status, data1, data2):
    #print(status, data1, data2)
    if(data1 == 110):
        #print(data2)
        scaleVolume = rescale(data2, xmin=0, xmax=127, ymin=-60, ymax=18)
        wx.CallAfter(midiVolume, time=1, arg=scaleVolume)
        
def midiVolume(time, arg):
    #print(arg)
    frm.midiVolumeChange(arg)
    frm.changeVolume(arg)
#call une fonction a chaque midi event    
rawMidi = RawMidi(event)
'''FIN Gestion Voume MIDI'''


if __name__ == '__main__':
    # Quand le module n'est pas importé
    # create the app, the frame, show it, and start the event loop.
    app = wx.App()
    #app.Maximize(True)
    frm = MainFrame(title='Ensemble Accéléromètre Électro', audio=_audio)
    frm.Show()
    app.MainLoop()
else: 
    #Si mon ui est ouvert depuis un fichier externe
    frm = MainFrame(title='Ensemble Accéléromètre Électro', audio=_audio)
    frm.Show()