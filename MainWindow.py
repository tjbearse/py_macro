import wx
from SpecialsDialog import SpecialsDialog
from time import sleep
import sendInputs as si
import KeySequence as ks

class Pymacro(wx.App):
	def OnInit(self):
		frame = PymacroMainFrame(None, 'Pymacro')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

		
class PymacroMainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400, 350))
		self.panel = wx.Panel(self, wx.ID_ANY)
		self.spec_dlg = SpecialsDialog(self, -1, self.OnSpecBtn)

		self.InitMenu()
		self.InitScript()
		self.InitButtons()
		self.Panelize()
		
		self.panel.Fit()
	
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
		self.script = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)		
		self.script.Fit()
			
	def InitButtons(self):
		""" Initialize the upper controls, Run, Delay and Repeat """
		'''Special'''
		self.spec_btn = wx.Button(self.panel, label='Spec')
		self.spec_btn.SetToolTipString('click to add a special item')
		self.spec_btn.Bind(wx.EVT_BUTTON, self.OnShowCustomDialog, self.spec_btn)
		'''Repeat'''
		self.repeat_label = wx.StaticText(self.panel, label='Repeat')
		self.repeat_ctrl = wx.SpinCtrl(self.panel, initial=1, size=(50, -1))
		self.repeat_ctrl.SetToolTipString('repeat entire sequence')
		
		'''Delay'''
		self.delay_label = wx.StaticText(self.panel, label='Delay')
		self.delay_ctrl = wx.SpinCtrl(self.panel, initial=3, size=(50, -1))
		self.delay_ctrl.SetToolTipString('set run delay')
		
		'''Run'''
		self.run_btn = wx.Button(self.panel, label='Run')
		self.run_btn.SetToolTipString('click to run macro')
		self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun, self.run_btn)
		
	def Panelize(self):
		""" Arranges all elements in the main panel of the window """
		
		innerbox = wx.BoxSizer(wx.HORIZONTAL)
		innerbox.Add(self.spec_btn, proportion=0,
					flag=wx.LEFT | wx.RIGHT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		''' Repeat '''
		innerbox.Add(self.repeat_label, proportion=0,
					flag=wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		innerbox.Add(self.repeat_ctrl, proportion=0,
					flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		''' Delay '''
		innerbox.Add(self.delay_label, proportion=0,
					flag=wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		innerbox.Add(self.delay_ctrl, proportion=0,
					flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		''' Run '''
		innerbox.Add(self.run_btn, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		
		outerbox = wx.BoxSizer(wx.VERTICAL)
		outerbox.Add(innerbox, flag=wx.ALIGN_LEFT | wx.ALIGN_RIGHT)
		outerbox.Add(self.script, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		self.panel.SetSizer(outerbox)
		
		mainsizer = wx.GridSizer()
		mainsizer.Add(self.panel, 1, wx.EXPAND)
		self.SetSizer(mainsizer)
		
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
		text = " {"+btn_name+"} "
		self.script.WriteText(text)
	
	def OnRun(self, e):
		print "running"
		# disable run btn
		self.run_btn.Unbind(wx.EVT_BUTTON)

		# parse
		#try:
		if self.script.IsModified():
			text = ''
			for line in xrange(0, self.script.GetNumberOfLines()):
				text += self.script.GetLineText(line)
			self.parsed = ks.Parse(text)
			self.script.SetModified(False)
		#except ks.ParseError:
			#IDK what to do here yet
		
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
		



app = Pymacro(False)
app.MainLoop()
