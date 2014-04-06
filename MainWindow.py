import wx
import SpecialsDialog as sd
from time import sleep
import sendInputs as si
import KeySequence as ks
import vkCodes as vk
import templateBox as tb

class Pymacro(wx.App):
	def OnInit(self):
		frame = PymacroMainFrame(None, 'Pymacro')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

		
class PymacroMainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.mainPanel = wx.Panel(self)
		self.specPanel = wx.Panel(self)
		self.runPanel = wx.Panel(self)
		self.spec_dlg = sd.SpecialsDialog(self, -1, self.OnSpecBtn)

		self.InitMenu()
		self.InitScript()
		self.InitButtons()
		self.InitMainPanel()
		self.InitRunPanel()
		self.InitSpecPanel()
		
		horizsizer = wx.BoxSizer(wx.HORIZONTAL)
		horizsizer.Add(self.mainPanel, 3, wx.EXPAND)
		horizsizer.Add(self.specPanel, 2, wx.EXPAND)
		
		vertsizer = wx.BoxSizer(wx.VERTICAL)
		vertsizer.Add(self.runPanel, 0, wx.EXPAND)
		vertsizer.Add(horizsizer, 1, wx.EXPAND)
		
		self.SetSizerAndFit(vertsizer)
		
	def InitMenu(self):
		""" initializes the menu bar and binds menu items to functions """
		self.CreateStatusBar()
		
		filemenu = wx.Menu()
		
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Info about this program")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		filemenu.AppendSeparator()
		
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Close the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

	
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)
		
		
	def InitScript(self):
		""" Initialize the list control containing the key sequences to run """
		self.script = wx.TextCtrl(self.mainPanel, style=wx.TE_MULTILINE)		
		self.script.Fit()
			
	def InitButtons(self):
		""" Initialize the upper controls, Run, Delay and Repeat """
		'''Repeat'''
		self.repeat_label = wx.StaticText(self.runPanel, label='Repeat')
		self.repeat_ctrl = wx.SpinCtrl(self.runPanel, initial=1, size=(50, -1))
		self.repeat_ctrl.SetToolTipString('repeat entire sequence')
		
		'''Delay'''
		self.delay_label = wx.StaticText(self.runPanel, label='Delay')
		self.delay_ctrl = wx.SpinCtrl(self.runPanel, initial=3, size=(50, -1))
		self.delay_ctrl.SetToolTipString('set run delay')
		
		'''Run'''
		self.run_btn = wx.Button(self.runPanel, label='Run')
		self.run_btn.SetToolTipString('click to run macro')
		self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun, self.run_btn)

	
	def InitRunPanel(self):
		""" Arranges all elements in the main mainPanel of the window """
		
		innerbox = wx.BoxSizer(wx.HORIZONTAL)
		innerbox.AddStretchSpacer(2)
		''' Repeat '''
		innerbox.Add(self.repeat_label, proportion=0,
					flag=wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP,
					border=10)
		innerbox.Add(self.repeat_ctrl, proportion=0,
					flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP,
					border=10)
		''' Delay '''
		innerbox.Add(self.delay_label, proportion=0,
					flag=wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP,
					border=10)
		innerbox.Add(self.delay_ctrl, proportion=0,
					flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP,
					border=10)
		''' Run '''
		innerbox.Add(self.run_btn, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP,
					border=10)
		innerbox.AddStretchSpacer(1)
		self.runPanel.SetSizer(innerbox)

		
	def InitMainPanel(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.script, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		self.mainPanel.SetSizer(sizer)
		
		mainsizer = wx.GridSizer()
		mainsizer.Add(self.mainPanel, 1, wx.EXPAND)
		self.SetSizer(mainsizer)

	
	def InitSpecPanel(self):
		''' TREE '''
		self.specTree = wx.TreeCtrl(self.specPanel,
								style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
		root = self.specTree.AddRoot("root")
		quote = self.specTree.AppendItem(root, "Quote")
		repeat = self.specTree.AppendItem(root, "Repeat")
		spec = self.specTree.AppendItem(root, "Special")
		for name in vk.Names:
			branch = self.specTree.AppendItem(spec, name[0])
			for item in name[1]:
# 				data = wx.TreeItemData(item[2])
				leaf = self.specTree.AppendItem(branch, item[0])  # , data=data)
		self.specTree.Expand(spec)

		''' TEMPLATE BOX '''
		self.template = tb.TemplateBox(self.specPanel, self.script)
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.specTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnActivate)
		sizer.Add(self.specTree, 4, wx.EXPAND | wx.ALL ^ wx.LEFT, 10)
		sizer.Add(self.template, 1, wx.EXPAND | wx.Right | wx.BOTTOM, 10)
		self.specPanel.SetSizer(sizer)
	'''
	Menu Event Handlers
	'''
	
	
	''' OTHER '''
	def OnShowCustomDialog(self, event):
		self.spec_dlg.Show()
		self.spec_dlg.SetFocus()
	
	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A small macro program written by TJ", "About Pymacro", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnExit(self, e):
		self.Close(True)
	
	'''
	Other Event Handlers
	'''
	def OnSpecBtn(self, event, btn_name):
		print btn_name
		text = " {" + btn_name + "} "
		self.script.WriteText(text)
	
	def OnRun(self, e):
		print "running"
		# disable run btn
		self.run_btn.Unbind(wx.EVT_BUTTON)

		# parse
		# try:
		if self.script.IsModified():
			text = ''
			for line in xrange(0, self.script.GetNumberOfLines()):
				text += self.script.GetLineText(line)
			self.parsed = ks.Parse(text)
			self.script.SetModified(False)
		# except ks.ParseError:
			# IDK what to do here yet
		
		# TODO: run this concurrently with parsing
		# count down
		sec = self.delay_ctrl.Value
		while sec != 0:
			self.run_btn.SetLabel(str(sec))
			sleep(1)
			sec -= 1
			
		
		for i in range(0, self.repeat_ctrl.GetValue()):
				self.run_btn.SetLabel('...(' + str(i) + ')')
				si.runSlow(self.parsed)
		
		self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun, self.run_btn)
		self.run_btn.SetLabel('Run')
		
	def OnActivate(self, event):
		item = event.GetItem()
		itemTxt = self.specTree.GetItemText(item)
		self.template.setTemplate(itemTxt)
		
		self.specPanel.Layout()
		


app = Pymacro(False)
app.MainLoop()
