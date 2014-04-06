import wx
import vkCodes as vk

class TemplateBox(wx.StaticBox):
    def __init__(self, parent, textCtrl):
        wx.StaticBox.__init__(self, parent, label="Template")
        self.beginText = wx.StaticText(self)
        self.spinCtrl = wx.SpinCtrl(self, size=(50, -1))
        self.choice = wx.Choice(self, size=(70, -1))
        self.textCtrl = wx.TextCtrl(self, size=(50, -1))
        self.midText = wx.StaticText(self)
        self.endText = wx.StaticText(self)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        flag = wx.SizerFlags().Border(wx.ALL ^ wx.RIGHT, 5).Center()
        sizer.AddStretchSpacer(1)
        sizer.AddF(self.beginText, flag)
        sizer.AddF(self.choice, flag)
        sizer.AddF(self.spinCtrl, flag)
        sizer.AddF(self.midText, flag)
        sizer.AddF(self.textCtrl, flag)
        sizer.AddF(self.endText, flag)
        sizer.AddStretchSpacer(1)
        
        
        self.beginText.Hide()
        self.spinCtrl.Hide()
        self.choice.Hide()
        self.midText.Hide()
        self.textCtrl.Hide()
        self.endText.Hide()
        
        self.btn = wx.Button(self, label="Add")
        self.btn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.target = textCtrl
        self.btn.Disable()
        self.AddText = None
        
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.AddSpacer(20)
        outer.Add(sizer, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        outer.AddStretchSpacer(1)
        outer.Add(self.btn, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.RIGHT | wx.BOTTOM, border=10)
        self.SetSizer(outer)
    
    def onAdd(self, e):
        self.AddText()
    
    def AddSpec(self):
        text = self.beginText.GetLabelText()
        text += self.choice.GetStringSelection()
        text += self.endText.GetLabelText()
        self.target.AppendText(text)
    
    def AddRep(self):
        text = self.beginText.GetLabelText()
        text += str(self.spinCtrl.GetValue())
        text += self.midText.GetLabelText()
        text += self.textCtrl.GetValue()        
        text += self.endText.GetLabelText()
        self.target.AppendText(text)
    
    def AddQuote(self):
        text = self.beginText.GetLabelText()
        text += self.textCtrl.GetValue()
        text += self.endText.GetLabelText()
        self.target.AppendText(text)
    
    def setTemplate(self, itemTxt):
        self.textCtrl.Clear()
        self.choice.Clear()
        self.spinCtrl.SetValue(0)
        
        if itemTxt in vk.Codes.keys():            
            self.AddText = self.AddSpec
            
            self.beginText.SetLabel("{" + itemTxt)
            self.choice.Clear()
            self.choice.AppendItems(['up', 'down', 'down up'])
            self.endText.SetLabel("}")

            self.btn.Enable()

            self.beginText.Show()
            self.spinCtrl.Hide()
            self.choice.Show()
            self.midText.Hide()
            self.textCtrl.Hide()
            self.endText.Show()
        elif itemTxt == 'Quote':
            self.AddText = self.AddQuote
            
            self.beginText.SetLabel('"')
            self.textCtrl.SetValue("")
            self.endText.SetLabel('"')
            
            self.btn.Enable()
            
            self.beginText.Show()
            self.spinCtrl.Hide()
            self.choice.Hide()
            self.midText.Hide()
            self.textCtrl.Show()
            self.endText.Show()
        elif itemTxt == 'Repeat':
            self.AddText = self.AddRep
            
            self.beginText.SetLabel('(')
            self.midText.SetLabel(', ')
            self.endText.SetLabel(')')
            
            self.btn.Enable()
            
            self.beginText.Show()
            self.spinCtrl.Show()
            self.choice.Hide()
            self.textCtrl.Show()
            self.midText.Show()
            self.endText.Show()
        else:
            self.btn.Disable()
            
            self.beginText.SetLabel("")
            self.spinCtrl.Hide()
            self.choice.Hide()
            self.midText.Hide()
            self.textCtrl.Hide()
            self.endText.SetLabel("")
            