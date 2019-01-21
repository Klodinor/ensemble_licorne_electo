"""
Hello World, but with more meat.
"""

import wx

class mainFrame(wx.Frame):
    """
    Main User Interface
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(mainFrame, self).__init__(*args, **kw)
        
        #Met l'interface en full screen
        self.Maximize()
        
        # create a panel in the frame - Panel s'insere dans le frame et permet de placer des elemets dessus
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundColour("#777777")#set la couleur du panel


        # and put some text with a larger bold font on it --> st = string, gere ce qui a trait au texte lui meme & font, tout ce qui a trait a la police de caractere 
        self.st = wx.StaticText(self.pnl, label="Ensemble Accéléromètre Électro", pos=(5,5))
        self.st.SetForegroundColour("#ffffff")
        self.font = self.st.GetFont()
        self.font.PointSize += 5
        #font = font.Bold()
        self.st.SetFont(self.font)

        # create a menu bar
        self.makeMenuBar()
        
        #initialise un slider
        '''sizer1 = self.createFreqSlider()'''

        # and a status bar -- un footer 
        self.CreateStatusBar()
        self.SetStatusText("Main User interface")


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


#if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
app = wx.App()
#app.Maximize(True)
frm = mainFrame(None, title='Ensemble Accéléromètre Électro')
frm.Show()
app.MainLoop()