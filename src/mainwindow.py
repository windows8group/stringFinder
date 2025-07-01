import wx

from src.funcs.reader import GetLanguagesList
from . import globs
from .views.unnamed import unnamedView
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.dirctrl import *
from libtextworker.interface.wx.miscs import CreateMenu

FilesUpdatedEvent, EVT_FILES_UPDATED = wx.lib.newevent.NewEvent()
DirsUpdatedEvent, EVT_DIRS_UPDATED = wx.lib.newevent.NewEvent()
OutputUpdatedEvent, EVT_OUTPUT_CHANGED = wx.lib.newevent.NewEvent()

class MainWindow(wx.Frame):
    
    filesBook: wx.Choicebook
    dirsBook : wx.Choicebook
    hasChanges: bool = False

    def __init__(this):
        wx.Frame.__init__(this, None, -1, "stringFinder")

        this.SetSize(800, 600)
        this.SetMinSize(wx.Size(800, 600))

        this.Bind(EVT_OUTPUT_CHANGED, this.RepopulateContent)
        this.Bind(wx.EVT_CLOSE, lambda _: this.TryToExit)
        this.PopulateBookContents()
        this.PopulateTheMenuBar()
        this.SetupStatusBar()

#region Content fillers
    def RepopulateContent(this, evt: FilesUpdatedEvent | DirsUpdatedEvent | OutputUpdatedEvent): # type: ignore
        if isinstance(evt, FilesUpdatedEvent):
            for path in evt.paths:
                this.filesBook.AddPage(unnamedView(this.filesBook, path), path)
            pass

        elif isinstance(evt, DirsUpdatedEvent):
            for path in evt.paths:
                this.dirsBook.AddPage(wx.Panel(this.dirsBook), path)
            pass

        elif isinstance(evt, OutputUpdatedEvent):
            this.filesBook.DeleteAllPages()
            this.dirsBook.DeleteAllPages()

            for file in globs.settings.source_files:
                this.filesBook.AddPage(unnamedView(this.filesBook, file), file)

            for dir in globs.settings.source_dirs:
                this.dirsBook.AddPage(wx.Panel(this.dirsBook), dir)
            
            this.StatusBar.SetStatusText(f"Output file: {globs.settings.output_dir}", 0)    

    def PopulateBookContents(this):
        sz = wx.BoxSizer()
        notebook = wx.Notebook(this)
        this.filesBook = wx.Choicebook(notebook)
        this.dirsBook = wx.Choicebook(notebook)

        # filesBook setup

        this.filesBook.Bind(EVT_FILES_UPDATED, this.RepopulateContent)
        this.filesBook.Bind(
            wx.EVT_CHOICEBOOK_PAGE_CHANGED,
            lambda _:
                this.StatusBar.SetStatusText(this.filesBook.GetPageText(this.filesBook.GetSelection()), 1)
        )

        for file in globs.settings.source_files:
            this.filesBook.AddPage(unnamedView(this.filesBook, file), file)

        notebook.AddPage(this.filesBook, "Input files")

        # dirsBook setup
        dirsSz = wx.BoxSizer()
        
        dirCtrl = DirCtrl(this.dirsBook, w_styles=DC_HIDEROOT | DC_USEICON)
        # dirCtrl.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, lambda evt: print(dir(evt)))
        
        for dir in globs.settings.source_dirs:
            dirCtrl.SetFolder(dir)
        
        # TODO: Handle directory events
        dirContent = wx.Panel(this.dirsBook)

        dirsSz.Add(dirCtrl, 1, wx.EXPAND)
        dirsSz.Add(dirContent, 1, wx.EXPAND)

        this.dirsBook.Bind(EVT_DIRS_UPDATED, this.RepopulateContent)
        this.dirsBook.SetSizerAndFit(dirsSz)
        
        notebook.AddPage(this.dirsBook, "Input dirs")

        # Place everything into the main sizer
        sz.Add(notebook, 1, wx.EXPAND)
        this.SetSizerAndFit(sz)
        notebook.Show()
    
    def PopulateTheMenuBar(this):
        menubar = wx.MenuBar()
        menubar.Append(CreateMenu(this,
            [
                (wx.ID_FILE, "Open file(s)", "", lambda _: this.OpenFileDlg(), wx.ITEM_NORMAL),
                (wx.ID_OPEN, "Open folder(s)", "", lambda _: this.OpenDirDlg(), wx.ITEM_NORMAL),
                (wx.ID_ANY,  "Select output folder", "", lambda _: this.GetOutputPaths(), wx.ITEM_NORMAL),
                (wx.ID_EXIT, "Exit", "Quit the application", lambda _: this.TryToExit(), wx.ITEM_NORMAL)
            ]
            ), "File"
        )

        locMenu = CreateMenu(this, [
            (500, "Force scan for languages", "No confirmation dialog!", \
             lambda _: this.ScanForLanguages(), wx.ITEM_NORMAL)
        ])

        locMenu.AppendSubMenu(CreateMenu(this,
            [ (1000 + i, globs.settings.languages[i], "", lambda _: (), wx.ITEM_NORMAL) for i in range(len(globs.settings.languages)) ]
        ), "Languages")

        menubar.Append(locMenu, "Localizations")

        menubar.Append(CreateMenu(this,
            [
                (wx.ID_ABOUT, "About", "", lambda _: this.ShowAboutDlg(), wx.ITEM_NORMAL)
            ]
            ), "Help"
        )
        this.SetMenuBar(menubar)
    
    def SetupStatusBar(this):
        statusBar = wx.StatusBar(this)
        statusBar.SetFieldsCount(2)
        statusBar.SetStatusText(f"Output directory: {globs.settings.output_dir}", 0)
        statusBar.SetStatusText(f"Current language: {...}", 1)

        this.SetStatusBar(statusBar)
#endregion

    def TryToExit(this):
        if wx.MessageBox("Save current settings? They are in+output paths, languages, and maybe more.", "Question",
                          style = wx.YES_NO | wx.CENTRE, parent = this) == wx.ID_YES:
            globs.settings.Update_And_Write()

    def ScanForLanguages(this):
        if len(globs.settings.languages) == 0 or wx.MessageBox(
            "This will override the current languages list!", "Confirmation",
            parent=this, style=wx.YES_NO | wx.CENTRE) == wx.ID_YES:
            globs.settings.languages = [l for l in GetLanguagesList()]


#region Dialogs
    def ShowAboutDlg(this):
        dlg = AboutDialog()
        dlg.SetDevelopers(["Windows8Group"])
        dlg.SetCopyright("(C) 2025 Windows8Group")
        dlg.SetName("stringFinder")
        dlg.ShowBox(this)
    
    def OpenFileDlg(this):
        with wx.FileDialog(this, style=wx.FD_FILE_MUST_EXIST | wx.FD_OPEN | wx.FD_MULTIPLE) as fileDlg:
            if fileDlg.ShowModal() == wx.ID_CANCEL:
                return
            
            globs.settings.source_files = fileDlg.GetPaths()
            this.GetOutputPaths()
            wx.PostEvent(this.filesBook, FilesUpdatedEvent(paths = fileDlg.GetPaths()))
    
    def OpenDirDlg(this):
        with wx.DirDialog(this, style=wx.DD_NEW_DIR_BUTTON | wx.DD_DIR_MUST_EXIST | wx.DD_MULTIPLE) as dirDlg:
            if dirDlg.ShowModal() == wx.ID_CANCEL:
                return
            
            globs.settings.source_dirs = dirDlg.GetPaths()
            this.GetOutputPaths()
            wx.PostEvent(this.filesBook, DirsUpdatedEvent(paths = dirDlg.GetPaths()))
    
    def GetOutputPaths(this):
        with wx.DirDialog(this, style=wx.DD_DIR_MUST_EXIST | wx.DD_NEW_DIR_BUTTON) as dirDlg:
            if dirDlg.ShowModal() == wx.ID_CANCEL:
                return
            
            globs.settings.output_dir = dirDlg.GetPath()
            this.ScanForLanguages()
            wx.PostEvent(this, OutputUpdatedEvent())
#endregion