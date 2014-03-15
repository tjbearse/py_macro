import wx
from wx.lib.mixins.listctrl import TextEditMixin

class Pymacro(wx.App):
	def OnInit(self):
		frame = PymacroMainFrame(None, 'Pymacro')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

class SequenceListCtrl(wx.ListCtrl, TextEditMixin):
	"""List style control for editing and displaying sequences of keys to run"""
	def __init__(self, parent, ID, pos=wx.DefaultPosition,
				size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		TextEditMixin.__init__(self) 
		self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnModified, self)

	''' methods '''
	def InsertNew(self, index=0):
		"""Inserts a new row, initialized to repeat=1 and blank sequence.
			rows are zero indexed
		"""
		assert(0 <= index <= self.GetItemCount())
		pos = self.InsertStringItem(index, '1');
		self.SetStringItem(pos, 1, '');

	def Delete(self, index):
		"""Deletes the specified row (zero indexed)"""
		assert(0 <= index <= self.GetItemCount())
		self.DeleteItem(index)

	'''Event Handlers'''
		
	def OnModified(self, event):
		print "modified: ", event.GetColumn(), ' ', event.GetText()
		
		
class PymacroMainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400, 350))
		self.panel = wx.Panel(self, wx.ID_ANY)

		self.InitMenu()
		self.InitScriptList()
		self.InitButtons()
		self.Panelize()
		
		self.panel.Fit()
		self.Fit()
	
	def InitMenu(self):
		""" initializes the menu bar and binds menu items to functions """
		self.CreateStatusBar()
		
		filemenu = wx.Menu()
		
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Info about this program")
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Close the program")
		

		editmenu = wx.Menu()
		insertmenu = wx.Menu()
		
		menu_insert_top = insertmenu.Append(wx.ID_ANY, "&Top", "Insert a row at the top of the list")
		menu_insert_bottom = insertmenu.Append(wx.ID_ANY, "&Bottom", "Insert a row at the bottom of the list")
		menu_insert_above = insertmenu.Append(wx.ID_ANY, "&Above Selected", "Insert a row above the selected row(s)")
		menu_insert_below = insertmenu.Append(wx.ID_ANY, "B&elow Selected", "Insert a row below the selected row(s)")		
		editmenu.AppendMenu(wx.ID_ANY, "&Insert", insertmenu)
		
		menuDelete = editmenu.Append(wx.ID_ANY, "&Delete", "Delete selected row(s)")
		
		
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(editmenu, "&Edit")
		self.SetMenuBar(menuBar)
		
		''' Bindings '''
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
	
		self.Bind(wx.EVT_MENU, self.OnInsertTop, menu_insert_top)
		self.Bind(wx.EVT_MENU, self.OnInsertBottom, menu_insert_bottom)
		self.Bind(wx.EVT_MENU, self.OnInsertAbove, menu_insert_above)
		self.Bind(wx.EVT_MENU, self.OnInsertBelow, menu_insert_below)
	
		self.Bind(wx.EVT_MENU, self.OnDelete, menuDelete)
		
	def InitScriptList(self):
		""" Initialize the list control containing the key sequences to run """
		self.scriptList = SequenceListCtrl(self.panel, wx.ID_ANY,
								style=wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.LC_VRULES | wx.LC_HRULES)		
		self.scriptList.InsertColumn(0, "Repetitions")
		self.scriptList.InsertColumn(1, "Sequence")
		self.scriptList.InsertNew()
		self.scriptList.Fit()
			
	def InitButtons(self):
		""" Initialize the upper controls, Run, Delay and Repeat """
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
		
	def Panelize(self):
		""" Arranges all elements in the main panel of the window """
		
		innerbox = wx.BoxSizer(wx.HORIZONTAL)
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
		innerbox.Add(self.run_btn, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
					border=10)
		
		outerbox = wx.BoxSizer(wx.VERTICAL)
		outerbox.Add(innerbox, flag=wx.ALIGN_LEFT | wx.ALIGN_RIGHT)
		outerbox.Add(self.scriptList, proportion=2, flag=wx.EXPAND | wx.ALL,
					border=10)
		self.panel.SetSizer(outerbox)
		

	'''
	Menu Event Handlers
	'''
	def OnInsertBottom(self, e):
		""" Insert a new row below the last row of the list control """
		print self.scriptList.GetEditControl()
		self.scriptList.InsertNew()
		
	def OnInsertTop(self, e):
		""" Insert a new row above the first row of the list control """
		self.scriptList.InsertNew(0)
		
	def OnInsertAbove(self, e):
		""" Insert a new row above the current selection """
		index = self.scriptList.GetFirstSelected()
		if index == -1: # no selection
			index = 0
		self.scriptList.InsertNew(index)
		
	def OnInsertBelow(self, e):
		""" Insert a new row below the current selection """
		index = self.scriptList.GetFirstSelected() + self.scriptList.GetSelectedItemCount()
		self.scriptList.InsertNew(index)
		
	def OnDelete(self, e):
		""" Deletes the selected rows """
		index = self.scriptList.GetFirstSelected()
		for x in xrange(self.scriptList.GetSelectedItemCount()):
			self.scriptList.Delete(index)
		if self.scriptList.GetItemCount() == 0:
			self.scriptList.InsertNew()
		
	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A small macro program written by TJ", "About Pymacro", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnExit(self, e):
		self.Close(True)
	
	# create the control buttons dialog
	# this is to input control sequences into workspace
	def initControlDialog(self):  # TODO: rename to mod
		""" this dialog holds buttons that will add the corresponding modifier to the sequence """
		None


app = Pymacro(False)
app.MainLoop()
