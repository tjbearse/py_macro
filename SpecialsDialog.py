import wx
from wx.lib.scrolledpanel import ScrolledPanel
import vkCodes as vk
import math

class SpecialsDialog(wx.Dialog):
    def __init__(self, parent, id, func):
        wx.Dialog.__init__(self, parent, id, "Special Items", size=(700, 500))
        self.panel = ScrolledPanel(self, style=wx.VSCROLL)
        self.OnButtonPress = func
        sizer = wx.BoxSizer(wx.VERTICAL)
        for name in vk.Names:
            CP = wx.CollapsiblePane(self.panel, -1, label=name[0])  
            CP.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)       
            win = CP.GetPane()        
            rows = math.ceil(len(name[1]) / 5.0) + 1
            pansizer = wx.GridSizer(rows=rows , cols=5, hgap=5, vgap=0)
            
            for btn in name[1]:
                spec_btn = wx.Button(CP.GetPane(), -1, btn[0])
                spec_btn.SetToolTipString(btn[1])
                pansizer.Add(spec_btn, 0, wx.ALL)
                spec_btn.Bind(wx.EVT_BUTTON, lambda evt, temp=btn[0]: self.OnButtonPress(evt, temp))
            pansizer.AddSpacer(10)
            win.SetSizer(pansizer)
            pansizer.SetSizeHints(win)
            sizer.Add(CP, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(sizer)
        self.panel.SetupScrolling(False, True)

        
    def OnPaneChanged(self, evt):
        # redo the layout
        self.panel.GetSizer().Layout()
        self.panel.FitInside()
    