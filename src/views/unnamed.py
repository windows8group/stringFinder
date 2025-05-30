import wx
import wx.propgrid
from wx.lib.agw import ultimatelistctrl as ULC
from ..funcs.microsuck import MicroSuck
from .. import globs

# Taken from wxdemo
class SingleChoiceDialogAdapter(wx.propgrid.PGEditorDialogAdapter):

    def __init__(self, choices):
        wx.propgrid.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid: wx.propgrid.PropertyGrid, property: wx.propgrid.PGProperty) -> bool:
        s = wx.GetSingleChoice("Pick one.", "Input string", self.choices)

        if s:
            self.SetValue(s)
            # property.SetCell(2, wx.propgrid.PGCell(propGrid.Parent.Parent.proj.comments[self.choices.index(s)])) # type: ignore
            return True

        return False

class SingleChoiceProperty(wx.propgrid.StringProperty):

    def __init__(self, label: str, choices: list[str]):
        wx.propgrid.StringProperty.__init__(self, label)
        
        self.dialog_choices = choices

    def DoGetEditorClass(self):
        return wx.propgrid.PGEditor_TextCtrlAndButton

    def GetEditorDialog(self):
        return SingleChoiceDialogAdapter(self.dialog_choices)
# End taken from wxdemo

class unnamedView(wx.Panel):

    proj: MicroSuck # TODO: Support other project types
    mgr: ULC.UltimateListCtrl
    targetFile: str

    def __init__(this, parent: wx.Window, target: str):
        wx.Panel.__init__(this, parent)
        this.targetFile = target
        this.proj = MicroSuck(target)
        this.PopulateContent()

    def PopulateContent(this):
        sz = wx.BoxSizer()

        this.mgr = ULC.UltimateListCtrl(
            this, agwStyle=wx.LC_REPORT | wx.LC_SINGLE_SEL |
                           wx.LC_AUTOARRANGE | ULC.ULC_SHOW_TOOLTIPS |
                           ULC.ULC_HAS_VARIABLE_ROW_HEIGHT |
                           ULC.ULC_HEADER_IN_ALL_VIEWS |
                           ULC.ULC_STICKY_HIGHLIGHT |
                           ULC.ULC_VRULES | ULC.ULC_HRULES |
                           wx.LC_MASK_SORT
        )
        this.mgr.InsertColumn(0, "Name")
        this.mgr.SetColumnWidth(0, 300)

        this.mgr.InsertColumn(1, "String")
        this.mgr.SetColumnWidth(1, 200)
        
        this.mgr.InsertColumn(2, "Translation")
        this.mgr.SetColumnWidth(2, 300)

        this.mgr.InsertColumn(3, "Comment")
        this.mgr.SetColumnWidth(3, 300)

        dlg = wx.ProgressDialog(
            this.targetFile, "Loading stuff...", maximum=len(this.proj.names),
            parent=this, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH
        )
        for i in range(len(this.proj.names)):
            dlg.Update(i, f"String name {i + 1}th: {this.proj.names[i]}")
            this.mgr.InsertStringItem(i, this.proj.names[i])
            this.mgr.SetStringItem(i, 0, this.proj.names[i])

            secondCol = this.mgr.GetItem(i, 1)
            secondCol.SetWindow(wx.ComboBox(this.mgr, choices=this.proj.inputs, style=wx.CB_DROPDOWN | wx.CB_READONLY, size=wx.Size(200, -1)))
            this.mgr.SetItem(secondCol)

            thirdCol = this.mgr.GetItem(i, 2)
            thirdCol.SetWindow(
                wx.TextCtrl(this.mgr, value = this.proj.translations[i], size=wx.Size(300, -1),
                            style = wx.TE_BESTWRAP | wx.TE_MULTILINE)
            )
            this.mgr.SetStringItem(i, 2, this.proj.translations[i])
            this.mgr.SetStringItem(i, 3, this.proj.comments[i])
            wx.YieldIfNeeded()
        
        dlg.Destroy()
        this.mgr.Refresh()
            
        sz.Add(this.mgr, 1, wx.EXPAND)
        this.SetSizerAndFit(sz)
