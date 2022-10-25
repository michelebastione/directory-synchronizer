import os, sys, wx, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Finestra(wx.Frame):
    def __init__(self, par = None, tit = "Sincronizzatore di cartelle", dim = (750, 200)):
        super(Finestra, self).__init__(par, title = tit, size = dim)
        self.Center()
        self.pannello = wx.Panel(self)
        self.pannello.SetBackgroundColour('white')
        self.carattere = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        wx.StaticText(self.pannello, label = 'Cartella di origine: ', pos = (10, 30)).SetFont(self.carattere)
        wx.StaticText(self.pannello, label = 'Cartella di destinazione: ', pos = (10, 80)).SetFont(self.carattere)
        self.ind_1 = wx.TextCtrl(self.pannello, pos = (250,30), size = (350, 25), style = wx.TE_READONLY)
        self.ind_2 = wx.TextCtrl(self.pannello, pos = (250,80), size = (350, 25), style = wx.TE_READONLY)
        self.b1 = wx.Button(self.pannello, label = "Sfoglia", pos = (625, 27))
        self.b2 = wx.Button(self.pannello, label = "Sfoglia", pos = (625, 77))
        self.b1.Bind(wx.EVT_BUTTON, self.bot_1)
        self.b2.Bind(wx.EVT_BUTTON, self.bot_2)
        self.b3 = wx.Button(self.pannello, label = "Sincronizza", pos = (350, 125))
        self.b3.Disable()
        self.b3.Bind(wx.EVT_BUTTON, self.sinc)
        self.Show()
        self.dir_1 = wx.DirDialog(self, 'Cartella di origine')
        self.dir_2 = wx.DirDialog(self, 'Cartella di destinazione')
        self.Bind(wx.EVT_CLOSE, self.quit)

    def bot_1(self, e):
        if self.dir_1.ShowModal() == wx.ID_OK:
            global cartella_origine
            cartella_origine = self.dir_1.GetPath()
            self.ind_1.SetLabel(cartella_origine)
        else:
            return None
        if not self.ind_2.IsEmpty():
            self.b3.Enable()

    def bot_2(self, e):
        if self.dir_2.ShowModal() == wx.ID_OK:
            global cartella_destinazione
            cartella_destinazione = self.dir_2.GetPath()
            self.ind_2.SetLabel(cartella_destinazione)
        else:
            return None
        if not self.ind_1.IsEmpty():
            self.b3.Enable()
            
    def sinc(self, e):
        if self.ind_1.GetValue() == self.ind_2.GetValue():
            wx.MessageDialog(self, message = "Le cartelle di origine e destinazione non possono coincidere!", caption = 'Errore!', style = wx.OK | wx.ICON_ERROR).ShowModal()
            return None
        wx.MessageDialog(self, message = 'Cartelle sincronizzate!', caption = "Operazione terminata", style = wx.OK | wx.ICON_WARNING).ShowModal()
        self.Destroy()

    def quit(self, e):
        sys.exit()


class Handler(FileSystemEventHandler):
    def on_modified(self, evt):
        for file in set(os.listdir(cartella_origine))-set(os.listdir(cartella_destinazione)):
            size = -1 
            orig = "\""+os.path.join(cartella_origine, file)+"\""
            dest = "\""+os.path.join(cartella_destinazione, file)+"\""
            while size != os.path.getsize(orig.strip("\"")):
                size = os.path.getsize(orig.strip("\""))
                time.sleep(1)
            subprocess.call(' '.join(['copy', orig, dest]), shell = True)


app = wx.App()
f=Finestra()
app.MainLoop()


evt_hnd = Handler()
obs = Observer()
obs.schedule(evt_hnd, cartella_origine, recursive = True)
obs.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    obs.stop()
obs.join()
