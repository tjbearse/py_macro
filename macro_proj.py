import tkinter as tk
from key_emulator import VK_CODE, VK_CODE_SHIFT, ESC_CHAR
import time

class App():
	def __init__(self):
		self.root = tk.Tk()
		self.initUI()
		self.initControlDialog()
		self.root.mainloop()
	
	# initialize the main window's UI elements
	def initUI(self):
		#
		#Top-Left
		#
		
		#spacer
		tk.Frame(width=10, height=10).grid(row=0)
		
		
		#text input for creating a task item
		self.stringEntry = tk.Text(self.root, height = 8, width = 30)
		self.stringEntry.grid(row=1, column=1, columnspan=8)
		
		
		#Button to pop up Control Char menu
		self.ctrlBtn = tk.Button(self.root, text="Add Control Char", command=self.addCntrl)
		self.ctrlBtn.grid(row=3, column=1, columnspan=2)
		

		#Bottom
		#Left
		
		#Task Repeat count
		tk.Label(self.root, text="Repeat:").grid(row=7, column=1)
		self.repeatSpinbox = tk.Spinbox(self.root, width=4, from_=1, to=1000)
		self.repeatSpinbox.grid(row=7, column=2)

		#
		#Bottom-Middle
		#
		
		#Count Down
		tk.Label(self.root, text="Count Down:").grid(row=7, column=3, columnspan=3)	
		self.countDownSpinbox = tk.Spinbox(self.root, width=4, from_=1, to=10)
		self.countDownSpinbox.grid(row=7, column=6)

		#
		#Bottom-Right
		#
		
		tk.Frame(width=10).grid(row=7, column = 7)
		
		#Run Button
		self.runBtn = tk.Button(self.root, text="Run", command=self.start)
		self.runBtn.grid(row=7, column=8)

		tk.Frame(height=10, width=10).grid(row=8, column = 9)
	
	# create the control buttons dialog
	# this is to input control sequences into workspace
	def initControlDialog(self): # TODO: rename to mod
		self.mod_box = tk.Toplevel(master=self.root)
		
		# don't close this, only want to hide it
		self.mod_box.protocol("WM_DELETE_WINDOW", self.hideControlDialog)
		
		row_n=0
		col_n=0
		listbox = tk.Listbox(master=self.mod_box)
		for btn in sorted(list(VK_CODE.keys())):
			listbox.insert(tk.END, btn)
			#button = tk.Button(master=self.box, text=btn)
			#button.grid(row=row_n, column=col_n)
			#col_n = int(col_n + 1) % 5
			#row_n += int(col_n / 4)
		listbox.pack()
		
		button = tk.Button(master=self.mod_box, text="OK", command=self.insertFromDialog)
		button.pack()
		
		self.mod_box.withdraw();
		
	# hide the modifiers box
	def hideControlDialog(self):
		self.mod_box.withdraw();
	
	# pop up the control dialog so user can select a btn to insert
	def addCntrl(self):
		self.mod_box.update();
		self.mod_box.deiconify();
		
	
	def insertFromDialog(self):
		print("insert from dialog")
		
			
	def start(self):
		self.count = int(self.countDownSpinbox.get())+1;
		self.update_clock()

	def update_clock(self):
		self.count-= 1
		if (self.count > 0):
			self.runBtn.configure(text=self.count)
			self.root.after(1000, self.update_clock)  
		else:
			self.runBtn.configure(text="Exec")
			self.run()
			self.runBtn.configure(text="Run")

	def run(self):
		print("run")
		try:
			for rep in range(0,  int(self.repeatSpinbox.get())):
				for i in range(0, self.listbox.size()):
					parse(self.listbox.get(i))
		except ParseError as e:
			print ("ParseError occurred: " + e.value)
	
class ParseError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)





# control characters will be written as <name u> <name d> <name t> <name> = cur mode
# syntax can also be used for other keys <n u> <d>

TAP = 1
UP = 2
DOWN = 3

MODE_CODE = {
	'u':UP,	'up':UP,
	't':TAP,	'tap':TAP,
	'd':DOWN,	'down':DOWN
}

def parse(string):
	index = 0
	mode = TAP
	escaped = False
	while(index < len(string)):	
		c = string[index]
		if(escaped):
			if( c not in ESC_CHAR):
				raise ParseError("Char "+str(c)+" not an esc char")
			esc = ESC_CHAR[c]
			simShift(esc, mode)
			escaped = False
		elif(c == '<'):
			# begin indivdual key element
			escaped_str = ""
			index += 1
			# get the whole thing
			while(string[index] != '>' and index != len(string)):
				escaped_str += string[index]
				index += 1
			
			# reached end without '>'
			if(index == len(string) and string[index-1] != '>'):
				raise ParseError("'<' bracket was not closed")
			
			# separate "name" and mode (if mode exists)
			split_str = escaped_str.split()
			if( len(split_str) > 2):
				raise ParseError("too many arguments, use: <key mode> or <key>")
			if( len(split_str) == 1):
				simShift(split_str, mode)
			else:
				m = MODE_CODE.get(split_str[1].lower(), TAP)
				simShift(split_str[0], m)
			
		elif(c == '\\'):
			escaped = True
		elif(c != ' '):
			simShift(c, mode)
		index += 1

def simShift(val, mode):
	if( val in VK_CODE):
		sim(VK_CODE[val], mode)
	elif( val in VK_CODE_SHIFT):
		keyDown(0x10) # shift
		keyTap(VK_CODE_SHIFT[val])
		keyUp(0x10) # end shift
	else:
		raise ParseError("Unknown char: '"+val+"'")

def sim(val, mode):
	if(mode == UP):
		keyUp(val)
	elif(mode == DOWN):
		keyDown(val)
	else:
		keyTap(val)
		
def keyTap(val):
	print ('t'+str(val))
	
def keyUp(val):
	print ('u'+str(val))
	
def keyDown(val):
	print ('d'+str(val))
	
app = App()