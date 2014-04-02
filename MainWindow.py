import wx
import SequenceListCtrl as sq
from time import sleep
import sendInputs as si

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
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		filemenu.AppendSeparator()
		
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Close the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		

		editmenu = wx.Menu()
		insertmenu = wx.Menu()
		
		menu_insert_top = insertmenu.Append(wx.ID_ANY, "&Top", "Insert a row at the top of the list")
		menu_insert_bottom = insertmenu.Append(wx.ID_ANY, "&Bottom", "Insert a row at the bottom of the list")
		menu_insert_above = insertmenu.Append(wx.ID_ANY, "&Above Selected", "Insert a row above the selected row(s)")
		menu_insert_below = insertmenu.Append(wx.ID_ANY, "B&elow Selected", "Insert a row below the selected row(s)")		
		self.Bind(wx.EVT_MENU, self.OnInsertTop, menu_insert_top)
		self.Bind(wx.EVT_MENU, self.OnInsertBottom, menu_insert_bottom)
		self.Bind(wx.EVT_MENU, self.OnInsertAbove, menu_insert_above)
		self.Bind(wx.EVT_MENU, self.OnInsertBelow, menu_insert_below)

		editmenu.AppendMenu(wx.ID_ANY, "&Insert", insertmenu)
		
		
		menuDelete = editmenu.Append(wx.ID_ANY, "&Delete", "Delete selected row(s)")
		
		movemenu = wx.Menu()
		menu_move_top = movemenu.Append(wx.ID_ANY, "&Top", "Move selected to the top of the list")
		menu_move_up = movemenu.Append(wx.ID_ANY, "&Up", "Move selected row up")
		menu_move_down = movemenu.Append(wx.ID_ANY, "&Down", "Move selected row down")
		menu_move_bottom = movemenu.Append(wx.ID_ANY, "&Bottom", "Move selected row down")
		self.Bind(wx.EVT_MENU, self.OnMoveTop, menu_move_top)
		self.Bind(wx.EVT_MENU, self.OnMoveUp, menu_move_up)
		self.Bind(wx.EVT_MENU, self.OnMoveDown, menu_move_down)
		self.Bind(wx.EVT_MENU, self.OnMoveBottom, menu_move_bottom)
		
		editmenu.AppendMenu(wx.ID_ANY, "&Move", movemenu)
		
		
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(editmenu, "&Edit")
		self.SetMenuBar(menuBar)
		
		self.Bind(wx.EVT_MENU, self.OnDelete, menuDelete)
		
	def InitScriptList(self):
		""" Initialize the list control containing the key sequences to run """
		self.scriptList = sq.SequenceListCtrl(self.panel, wx.ID_ANY,
								style=wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.LC_VRULES | wx.LC_HRULES)		
		self.scriptList.InsertColumn(0, "Sequence")
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
		self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun, self.run_btn)
		
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
		
	''' INSERTS '''
	def OnInsertBottom(self, e):
		""" Insert a new row below the last row of the list control """
		self.scriptList.InsertNew(self.scriptList.GetItemCount() - 1)
		
	def OnInsertTop(self, e):
		""" Insert a new row above the first row of the list control """
		self.scriptList.InsertNew(0)
		
	def OnInsertAbove(self, e):
		""" Insert a new row above the current selection """
		index = self.scriptList.GetFirstSelected()
		if index == -1:  # no selection
			index = 0
		self.scriptList.InsertNew(index)
		
	def OnInsertBelow(self, e):
		""" Insert a new row below the current selection """
		index = self.scriptList.GetFirstSelected() + self.scriptList.GetSelectedItemCount()
		if index == -1:
			index = self.scriptList.GetItemCount() - 1
		self.scriptList.InsertNew(index)
		
	
	''' DELETES '''
	def OnDelete(self, e):
		""" Deletes the selected rows """
		index = self.scriptList.GetFirstSelected()
		for usused in xrange(self.scriptList.GetSelectedItemCount()):
			self.scriptList.Delete(index)
		if self.scriptList.GetItemCount() == 0:
			self.scriptList.InsertNew()
		
		
	''' MOVES '''
	def OnMoveUp(self, e):
		index = self.scriptList.GetFirstSelected()
		if index != -1 and index != 0 and index != self.scriptList.GetItemCount():
			self.scriptList.Select(index, False)
			self.scriptList.Move(index, index - 1)
			self.scriptList.Select(index - 1, True)
		
	
	def OnMoveDown(self, e):
		index = self.scriptList.GetFirstSelected()
		if index != -1 and index != self.scriptList.GetItemCount() - 1 and index != self.scriptList.GetItemCount():
			self.scriptList.Select(index, False)
			self.scriptList.Move(index, index + 1)
			self.scriptList.Select(index + 1, True)

	def OnMoveTop(self, e):
		index = self.scriptList.GetFirstSelected()
		if index != -1 and index != 0 and index != self.scriptList.GetItemCount():
			self.scriptList.Select(index, False)
			self.scriptList.Move(index, 0)
			self.scriptList.Select(0, True)
		
	def OnMoveBottom(self, e):
		index = self.scriptList.GetFirstSelected()
		if index != -1 and index != self.scriptList.GetItemCount() - 1 and index != self.scriptList.GetItemCount():
			self.scriptList.Select(index, False)
			self.scriptList.Move(index, self.scriptList.GetItemCount() - 1)
			self.scriptList.Select(self.scriptList.GetItemCount() - 2, True)
		
		
	''' OTHER '''
	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A small macro program written by TJ", "About Pymacro", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnExit(self, e):
		self.Close(True)
	
	'''
	Other Event Handlers
	'''
	
	def OnRun(self, e):
		print "running"
		sec = self.delay_ctrl.Value
		while sec != 0:
			self.run_btn.SetLabel(str(sec))
			sleep(1)
			sec -= 1
		self.run_btn.Unbind(wx.EVT_BUTTON)
		for i in range(0, self.repeat_ctrl.GetValue()):
			self.run_btn.SetLabel('...(' + str(i) + ')')
 			for row in self.scriptList.sequences:
 				print row.parsed
 				si.runSlow(row.parsed)
		self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun, self.run_btn)
		self.run_btn.SetLabel('Run')
		
	# create the control buttons dialog
	# this is to input control sequences into workspace
	def initControlDialog(self):  # TODO: rename to mod
		""" this dialog holds buttons that will add the corresponding modifier to the sequence """
		None


app = Pymacro(False)
app.MainLoop()
