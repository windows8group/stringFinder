import wx
import wx.adv
from .. import globs

class LanguagesEditor(wx.Dialog):
    elb: wx.adv.EditableListBox

    def __init__(this, parent: wx.Window):
        wx.Dialog.__init__(this, parent, title="Languages to be generated")
        
        panel = wx.Panel(this)
        this.elb = wx.adv.EditableListBox(
            panel, label="Language codes (e.g en-US)",
            style=wx.adv.EL_DEFAULT_STYLE | wx.adv.EL_ALLOW_NEW |
                  wx.adv.EL_ALLOW_EDIT | wx.adv.EL_ALLOW_DELETE
        )
        this.elb.SetStrings(globs.settings.languages)
    
    def Close(this, force: bool = False) -> bool:
        globs.settings.languages = this.elb.GetStrings()
        return wx.Dialog.Close(this, force)