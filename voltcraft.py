from Tkinter import *
from ScrolledText import ScrolledText
import tkFileDialog

import subprocess
import os
import grp

class Content(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, width=400, height=400)
		
		self.master = master
		
		self.pack_propagate(0)
		
		self.pack(side=RIGHT)

class Menu(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, width=100, height=400)
		
		self.master = master
		
		self.pack_propagate(0)
		
		self.pack(side=LEFT)
		
		self.init()
	
	def init(self):
		self.buttonConfigure = Button(self, width=90, text="Configure", command=self.configure)
		self.buttonConfigure.pack()
	
		self.buttonPrintData = Button(self, width=90, text="Data", command=self.data)
		self.buttonPrintData.pack()
	
	def configure(self):
		self.master.content.destroy()
		self.master.content = Content(self.master)
		
		self.master.content.labelLogname = Label(self.master.content, text='Name of log file')
		self.master.content.labelLogname.pack()
		self.master.content.entryLogname = Entry(self.master.content)
		self.master.content.entryLogname.pack()
		
		self.master.content.labelNumData = Label(self.master.content, text='Number of data points (max 16 000)')
		self.master.content.labelNumData.pack()
		self.master.content.entryNumData = Entry(self.master.content)
		self.master.content.entryNumData.pack()
		
		self.master.content.labelInterval = Label(self.master.content, text='Interval (in seconds)')
		self.master.content.labelInterval.pack()
		self.master.content.entryInterval = Entry(self.master.content)
		self.master.content.entryInterval.pack()
		
		
		self.master.content.buttonSaveConfig = Button(self.master.content, text="Save config", command=self.saveConfig)
		self.master.content.buttonSaveConfig.pack()


		stdout, stderr = subprocess.Popen(['vdl120', '-i'], stdout=subprocess.PIPE).communicate()

		self.master.content.labelStatus = Label(self.master.content, justify=LEFT, font=('Monospace', '8'), text=stdout)
		self.master.content.labelStatus.pack()
	
	def saveConfig(self):
		logname = self.master.content.entryLogname.get()
		numdata = self.master.content.entryNumData.get()
		interval = self.master.content.entryInterval.get()
		
		stdout, stderr = subprocess.Popen(['vdl120', '-c', logname, numdata, interval], stdout=subprocess.PIPE).communicate()

		self.master.content.labelStatus.destroy()
		self.master.content.labelStatus = Label(self.master.content, justify=LEFT, font=('Monospace', '8'), text=stdout)
		self.master.content.labelStatus.pack()
	
	def data(self):
		self.master.content.destroy()
		self.master.content = Content(self.master)
		
		stdout, stderr = subprocess.Popen(['vdl120', '-p'], stdout=subprocess.PIPE).communicate()
		
		self.master.content.text = ScrolledText(self.master.content)
		self.master.content.text.insert(INSERT, stdout)
		self.master.content.text.pack()
		
		self.master.content.buttonSaveData = Button(self.master.content, text="Save", command=lambda: self.saveData(stdout))
		self.master.content.buttonSaveData.pack()		
		
	def saveData(self, data):
		fileName = tkFileDialog.asksaveasfilename(master=self.master, filetypes=[('all files', '.*'), ('dat files', '.dat')])
		if fileName:
			f = open(fileName, 'w')
			f.write(data)
			f.close()
			
			user = os.environ['SUDO_USER']
			gid = os.environ['SUDO_GID']
			group = grp.getgrgid(gid)[0]

			subprocess.call(['chown', user, fileName])
			subprocess.call(['chgrp', group, fileName])
			
	

class Application(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, width=500, height=400)
		
		self.master = master
		
		self.pack_propagate(0)
		
		self.pack()
		
		self.menu = Menu(self)
		self.content = Content(self)
		self.content.label = Label(self.content, text="Voltcraft DL-120TH data logger")
		self.content.label.pack()
	
	
	



def main():
	root = Tk()
	
	root.title("Voltcraft")
	
	app = Application(root)
	
	root.mainloop()

if __name__ == "__main__":
	main();
