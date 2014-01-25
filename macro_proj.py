import tkinter as tk
import win32api
import win32con; dir(win32con)
import key_emulator
import time

class App():
	def __init__(self):
		self.root = tk.Tk()
		self.initUI()
		self.initControlDialog()
		self.root.mainloop()
		
	def initUI(self):
		#Top-Left
		tk.Frame(width=10, height=10).grid(row=0)

		self.stringEntry = tk.Entry(self.root)
		self.stringEntry.grid(row=2, column=1, columnspan=2)

		self.ctrlBtn = tk.Button(self.root, text="Add Control Char", command=self.addCntrl)
		self.ctrlBtn.grid(row=3, column=1, columnspan=2)
		#Top-Middle
		tk.Frame(width=10).grid(row=0, column=3)

		self.upBtn = tk.Button(self.root, text="Up", command=self.up)
		self.upBtn.grid(row=2, column=4)

		self.downBtn = tk.Button(self.root, text="Down", command=self.down)
		self.downBtn.grid(row=3, column=4)
		
		self.insertBtn = tk.Button(self.root, text=">>", command=self.insert)
		self.insertBtn.grid(row=4, column=4)
		self.removeBtn = tk.Button(self.root, text="<<", command=self.remove)
		self.removeBtn.grid(row=5, column=4)
		#Top-Right
		tk.Frame(width=10).grid(row=0, column=5)

		self.listbox = tk.Listbox(self.root)
		self.listbox.grid(row=1, rowspan=5, column=6, columnspan=3, sticky=tk.N)

		tk.Frame(width=10, height=10).grid(row=6, column=9)

		#Bottom-left
		tk.Label(self.root, text="Repeat:").grid(row=7, column=1)
		self.repeatSpinbox = tk.Spinbox(self.root, width=4, from_=1, to=1000)
		self.repeatSpinbox.grid(row=7, column=2)

		#Bottom-Middle
		tk.Label(self.root, text="Count Down:").grid(row=7, column=3, columnspan=3)	
		self.countDownSpinbox = tk.Spinbox(self.root, width=4, from_=1, to=10)
		self.countDownSpinbox.grid(row=7, column=6)

		#Bottom-Right
		self.runBtn = tk.Button(self.root, text="Run", command=self.start)
		self.runBtn.grid(row=7, column=8)

		tk.Frame(height=10).grid(row=8)
		
	def initControlDialog(self):
		self.box = tk.Toplevel(master=self.root)
		self.box.protocol("WM_DELETE_WINDOW", self.hideControlDialog)
		
		row_n=0
		col_n=0
		listbox = tk.Listbox(master=self.box)
		for btn in sorted(list(VK_CODE.keys())):
			listbox.insert(tk.END, btn)
			#button = tk.Button(master=self.box, text=btn)
			#button.grid(row=row_n, column=col_n)
			#col_n = int(col_n + 1) % 5
			#row_n += int(col_n / 4)
		listbox.pack()
		
		button = tk.Button(master=self.box, text="OK", command=self.insertFromDialog)
		button.pack()
		
	def hideControlDialog(self):
		print("hide")
		
	def addCntrl(self):
		print("show")
		
	def insertFromDialog(self):
		print("insert from dialog")
		
	def insert(self):
		text = self.stringEntry.get()
		if( len(text) != 0 ):
			self.stringEntry.delete(0, tk.END)
			self.listbox.insert(tk.END, text)
			self.listbox.see(tk.END)
		
	def remove(self):
		text = self.listbox.get(self.listbox.index(tk.ACTIVE))
		self.listbox.delete(self.listbox.index(tk.ACTIVE))

		self.stringEntry.delete(0, tk.END);
		self.stringEntry.insert(tk.END, text);
		
	def up(self):
		index = self.listbox.index(tk.ACTIVE)
		if(index != 0 and self.listbox.size() != 1):
			text = self.listbox.get(index)
			self.listbox.delete(index)
			self.listbox.insert(index-1, text)
			self.listbox.activate(index-1)
			
	def down(self):
		index = self.listbox.index(tk.ACTIVE)
		if(index != self.listbox.index(tk.END) and self.listbox.size() != 1):
			text = self.listbox.get(index)
			self.listbox.delete(index)
			self.listbox.insert(index+1, text)
			self.listbox.activate(index+1)
			
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
	
VK_CODE = {
	'backspace':0x08,		'tab':0x09,			'clear':0x0C,
	'enter':0x0D,		'shift':0x10,		'ctrl':0x11,
	'alt':0x12,			'pause':0x13,		'caps_lock':0x14,
	'esc':0x1B,			'spacebar':0x20,		'page_up':0x21,
	'page_down':0x22,		'end':0x23,			'home':0x24,
	'left_arrow':0x25,	'up_arrow':0x26,		'right_arrow':0x27,
	'down_arrow':0x28,	'select':0x29,		'print':0x2A,
	'execute':0x2B,		'print_screen':0x2C,	'ins':0x2D,
	'del':0x2E,			'help':0x2F,
	
	'0':0x30,	'1':0x31,	'2':0x32,	'3':0x33,	'4':0x34,
	'5':0x35,	'6':0x36,	'7':0x37,	'8':0x38,	'9':0x39,
	
	'a':0x41,	'b':0x42,	'c':0x43,	'd':0x44,	'e':0x45,
	'f':0x46,	'g':0x47,	'h':0x48,	'i':0x49,	'j':0x4A,
	'k':0x4B,	'l':0x4C,	'm':0x4D,	'n':0x4E,	'o':0x4F,
	'p':0x50,	'q':0x51,	'r':0x52,	's':0x53,	't':0x54,
	'u':0x55,	'v':0x56,	'w':0x57,	'x':0x58,	'y':0x59,
	'z':0x5A,
	
	'numpad_0':0x60,	'numpad_1':0x61,	'numpad_2':0x62,
	'numpad_3':0x63,	'numpad_4':0x64,	'numpad_5':0x65,
	'numpad_6':0x66,	'numpad_7':0x67,	'numpad_8':0x68,
	'numpad_9':0x69,
	
	'multiply_key':0x6A,	'add_key':0x6B,	'separator_key':0x6C,
	'subtract_key':0x6D,	'decimal_key':0x6E,	'divide_key':0x6F,
	
	'F1':0x70,	'F2':0x71,	'F3':0x72,	'F4':0x73,	'F5':0x74,
	'F6':0x75,	'F7':0x76,	'F8':0x77,	'F9':0x78,	'F10':0x79,
	'F11':0x7A,	'F12':0x7B,	'F13':0x7C,	'F14':0x7D,	'F15':0x7E,
	'F16':0x7F,	'F17':0x80,	'F18':0x81,	'F19':0x82,	'F20':0x83,
	'F21':0x84,	'F22':0x85,	'F23':0x86,	'F24':0x87,
	
	'num_lock':0x90,			'scroll_lock':0x91,
	'left_shift':0xA0,		'right_shift ':0xA1,
	'left_control':0xA2,		'right_control':0xA3,
	'left_menu':0xA4,			'right_menu':0xA5,
	'browser_back':0xA6,		'browser_forward':0xA7,
	'browser_refresh':0xA8,		'browser_stop':0xA9,
	'browser_search':0xAA,		'browser_favorites':0xAB,
	'browser_start_and_home':0xAC,'volume_mute':0xAD,
	'volume_Down':0xAE,		'volume_up':0xAF,
	'next_track':0xB0,		'previous_track':0xB1,
	'stop_media':0xB2,		'play/pause_media':0xB3,
	'start_mail':0xB4,		'select_media':0xB5,
	'start_application_1':0xB6,	'start_application_2':0xB7,
	'attn_key':0xF6,	'crsel_key':0xF7,	'exsel_key':0xF8,
	'play_key':0xFA,	'zoom_key':0xFB,	'clear_key':0xFE,
	
	'+':0xBB,	',':0xBC,	'-':0xBD,	'.':0xBE,
	'/':0xBF,	'`':0xC0,	';':0xBA,	'[':0xDB,
	'\\':0xDC,	']':0xDD,	"'":0xDE,
}

VK_CODE_SHIFT = {
	')':0x30,	'!':0x31,	'@':0x32,	'#':0x33,	'$':0x34,
	'%':0x35,	'^':0x36,	'&':0x37,	'*':0x38,	'(':0x39,
	
	'A':0x41,	'B':0x42,	'C':0x43,	'D':0x44,	'E':0x45,
	'F':0x46,	'G':0x47,	'H':0x48,	'I':0x49,	'J':0x4A,
	'K':0x4B,	'L':0x4C,	'M':0x4D,	'N':0x4E,	'O':0x4F,
	'P':0x50,	'Q':0x51,	'R':0x52,	'S':0x53,	'T':0x54,
	'U':0x55,	'V':0x56,	'W':0x57,	'X':0x58,	'Y':0x59,
	'Z':0x5A,
	
	'<':0xBC,	'_':0xBD,	'>':0xBE,	'?':0xBF,	'~':0xC0,
	':':0xBA,	'{':0xDB,	'|':0xDC,	'}':0xDD,	'"':0xDE,
}		

ESC_CHAR = {
	' ':0x20,	'\\':0xDC, '<':0xBC
}



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