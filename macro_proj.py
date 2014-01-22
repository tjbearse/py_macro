import tkinter as tk

import time

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.initUI()

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
        self.runBtn = tk.Button(self.root, text="Run", command=self.run)
        self.runBtn.grid(row=7, column=8)

        tk.Frame(height=10).grid(row=8)
        self.root.mainloop()


    def addCntrl(self):
        return 0
    def insert(self):
        text = self.stringEntry.get()
        self.stringEntry.delete(0, tk.END)
        
        self.listbox.insert(tk.END, text)
        
    def remove(self):
        return 0
    def up(self):
        return 0
    def down(self):
        return 0
    def run(self):
        return 0
"""
        self.button = tk.Button(self.root, text="run", command=self.update_clock)
        self.panel.add(self.button)

        self.delay = 3
        self.count = self.delay

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()
        self.listbox.insert(tk.END, "...")
        self.list = []
    def update_clock(self):
        self.count-= 1
        if (self.count > 0):
            self.button.configure(text=self.count)
            self.root.after(1000, self.update_clock)
        else:
            self.count = self.delay
            self.button.configure(text="run")
"""

app=App()
app.mainloop()
