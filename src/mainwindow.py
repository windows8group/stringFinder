import wx
import globs
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.miscs import CreateMenu

class MainWindow(wx.Frame):
    
    nb: wx.Choicebook

    def __init__(this):
        wx.Frame.__init__(this, None, -1, "stringFinder")

        this.PopulateTheMenuBar()
        this.SetupStatusBar()

        this.nb = wx.Choicebook(this)

        for file in globs.filesToUse:
            wind = wx.Panel()
            this.nb.AddPage(wind, file)
        
        this.nb.AddPage(wx.Panel(), "Untitled")

        for dir in globs.dirsToUse:
            wind = wx.Panel()
            this.nb.AddPage(wind, dir)
    
    def PopulateTheMenuBar(this):
        menubar = wx.MenuBar()
        menubar.Append(CreateMenu(this,
            [
                (wx.ID_FILE, "Open file(s)", "", lambda _: print(), wx.ITEM_NORMAL),
                (wx.ID_OPEN, "Open folder(s)", "", lambda _: print(), wx.ITEM_NORMAL),
                (wx.ID_EXIT, "Exit", "", lambda _: this.TryToExit(), wx.ITEM_NORMAL)
            ]
            ), "File"
        )
        menubar.Append(CreateMenu(this,
            [
                (wx.ID_ABOUT, "About", "", lambda _: this.ShowAboutDlg(), wx.ITEM_NORMAL)
            ]
            ), "Help"
        )
        this.SetMenuBar(menubar)
    
    def SetupStatusBar(this):
        statusBar = wx.StatusBar(this)
        statusBar.SetFieldsCount(3)
        this.SetStatusBar(statusBar)

    def TryToExit(this):
        ...

    def ShowAboutDlg(this):
        dlg = AboutDialog()
        dlg.SetDevelopers(["Windows8Group"])
        dlg.SetCopyright("(C) 2025 Windows8Group")
        dlg.SetName("stringFinder")
        dlg.ShowBox(this)