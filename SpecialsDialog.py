import wx
from wx.lib.scrolledpanel import ScrolledPanel
import vkCodes as vk
import math

class SpecialsDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, "Special Keys", size=(600, 600))
        self.panel = ScrolledPanel(self)
        self.panel.BackgroundColour = (0, 255, 144)
        vert = wx.BoxSizer(wx.VERTICAL)
        for name in vk.Names:
            collpane = wx.CollapsiblePane(self.panel, label=name[0])
            collpane.Collapse()
            collpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnChange(), collpane)
            vert.Add(collpane, 0, wx.GROW | wx.EXPAND, 5)
            rows = math.ceil(len(name[1])/5.0)
            sizer = wx.GridSizer(rows=rows , cols=5, hgap=5, vgap=0)
            for btn in name[1]:
    #                 print btn
                spec_btn = wx.Button(collpane.GetPane(), label=btn[0], size=(-1, -1))
                spec_btn.SetToolTipString(btn[1])
                sizer.Add(spec_btn, flag=wx.ALIGN_CENTER|wx.GROW)
            collpane.GetPane().SetSizer(sizer)
            sizer.SetSizeHints(collpane.GetPane())
        
            #spec_btn.Bind(wx.EVT_BUTTON, self.OnShowCustomDialog, spec_btn)
        self.panel.SetSizer(vert)
        
    def OnChange(self):
        print "there"