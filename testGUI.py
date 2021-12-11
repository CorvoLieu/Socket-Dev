from cgitb import text
from dataclasses import Field
from typing import Literal
from contact import *
import tkinter as tk
import random
from PIL import Image, ImageTk

test1 = Contact("Hao", "00001", "12345", "1mail", b'')
test2 = Contact("Thai", "00002", "12345", "2mail", b'')
testList1 = [test1, test2, test1, test2, test1, test2]
testList2 = [test1, test2]

Grey = "#E8E8E8"
LightGrey = "#f0f0f0"
Navy = "#14279B"
Bluely = "#3D56B2"
SkyBlue = "#5C7AEA"

mainWindow = tk.Tk()

#main window
mainWindow.title("Phone Book")
mainWindow.geometry("1000x600")
mainWindow.resizable(height=False, width=False)

#Background
mainCanvas = tk.Canvas(mainWindow,  width=1000,
						height=600, bg=Bluely)
mainCanvas.pack()

#Foreground
inputFrame = tk.Frame(mainCanvas, bg= LightGrey)
inputFrame.place(relwidth=0.96, relheight=0.94, relx=0.02, rely=0.03)

class InfoBar():
	def __init__(self, parrent, width, name: str, phone: str, mail: str, id: str) -> None:
		mainBar = tk.Frame(parrent, width=width, height=100, bg= Grey)
		mainBar.pack(padx=5, pady=5)
		self.width = width
		self.height = 100
		self.id = id

        #Labels
		self.name = tk.Label(mainBar, text="Name: " + name,
                             font=('Arial Bold', 12), anchor=tk.W, bg=Grey, fg="black")
		self.phone = tk.Label(mainBar, text="Number: " +
                              phone, font=('Arial', 12), anchor=tk.W, bg=Grey, fg="black")
		self.mail = tk.Label(mainBar, text="Email: " + mail,
                             font=('Arial', 12), anchor=tk.W, bg=Grey, fg="black")
		self.id = tk.Label(mainBar, text="ID: " + id,
                           font=('Arial Italic', 12), anchor=tk.W, bg=Grey, fg="black")

        # Button "View Avatar"
		avaBttn = tk.Button(mainBar, text="View Avatar",anchor= tk.W, command= lambda: MainGUI.ViewAva(id), bg=Bluely, fg="white")

        #Pic holder
		self.picPlace = tk.Canvas(mainBar, bg= '#7e7e7e', width= 80, height= 80)
		img = ImageTk.PhotoImage(Image.open(f"client\\{id}.jpg").resize((80, 80)))   #Temporally using 00001.jpg for testing
		photo = tk.Label(self.picPlace, image= img)
		photo.image = img
		photo.pack()

		#Placement
		self.name.place(x=self.width / 3 + 10, y= self.height / 4, anchor= tk.W)
		self.id.place(x=self.width - 80, y=self.height / 4, anchor= tk.W)
		self.phone.place(x=self.width / 3 + 10, y=self.height / 4 * 2, anchor= tk.W)
		self.mail.place(x=self.width / 3 + 10, y=self.height / 4 * 3, anchor= tk.W)
		avaBttn.place(x=self.width - 80, y=self.height - 20, anchor=tk.W)
		self.picPlace.place(x= self.width / 12, y= self.height / 2, anchor=tk.W)            


class InfoBox():
    def __init__(self, parrent, width, x=0, y=0, lst: list = []) -> None:
        self.width = width
        self.lst = lst

        #Config
        self.container = tk.Frame(parrent)
        self.mainBox = tk.Canvas(self.container, width=width, height=480, bg= LightGrey)
        self.mainBox.pack_propagate(0)

        self.scrol = tk.Scrollbar(self.container, command= self.mainBox.yview)
        self.scrollableFrame = tk.Frame(self.mainBox)

        self.scrollableFrame.bind("<Configure>", lambda e: self.mainBox.configure(scrollregion=self.mainBox.bbox("all")))

        self.mainBox.create_window((0, 0), window= self.scrollableFrame, anchor= tk.NW)
        self.mainBox.config(yscrollcommand= self.scrol.set)

        #FRAME  ->  CANVAS  ->  FRAME
        #  ^          ^           ^
        #Attach    Restrict     Scrollable
        #Scrollbar  the field

        #Placement
        self.container.place(x=x, y=y)
        self.mainBox.pack(side= tk.LEFT, fill= tk.BOTH, expand= True)
        self.scrol.pack(side = tk.RIGHT, fill= tk.Y)

    def createBar(self, contact: Contact):
        newBar = InfoBar(self.scrollableFrame, self.width - 10, contact.getName(),
                         contact.getPhone(), contact.getEmail(), contact.getID())

    def newList(self, lst: list):
        self.lst = lst
    
    def refeshBox(self):
        self.scrollableFrame.pack_forget()
        for widget in self.scrollableFrame.winfo_children():
            widget.destroy()
        
        for contact in self.lst:
            self.createBar(contact)



class MainGUI():
	def __init__(self) -> None:
        
		self.lst = testList1
		
		#Phone book text
		phoneBookText = tk.Label(inputFrame, text='fonebook', font=("Arial Black", 40), fg= Bluely, bg = LightGrey)
		phoneBookText.place(x=30, y=10)

		#List Box
		self.listBox = InfoBox(inputFrame, 450, 470, 75)
		self.listBox.newList(testList1)
		self.listBox.refeshBox()

		#Test Button
		refreshbttn = tk.Button(inputFrame, text= "Refresh", command= self.listBox.refeshBox)
		refreshbttn.place (x= 362, y= 123)

		##Search bar
		#Label
		srcLabel = tk.Label(
			inputFrame, text="Name", font=("Arial", 11), bg= LightGrey, fg="black"
		)
		srcLabel.place(x= 34, y= 100)


		#Bar
		srcBox = tk.Entry(
			inputFrame,  width=44
		)
		#srcBox.place(x=85, y=106)
		srcBox.place(x=36, y=126)

		#Button
		srcBttn = tk.Button(
			inputFrame, text="Search", bg=Bluely, fg="white", command= MainGUI.search
		)
		srcBttn.place (x=310, y=123)

		mainWindow.mainloop()

	def switchList(self):
		self.lst = testList2
		self.listBox.newList(testList2)
		self.listBox.refeshBox()
		
	def search():
		print("hello")


	def ViewAva(id: str):
		frame = tk.Frame(inputFrame, width=300, height=300, bg= "#" + str(random.randint(0, 9)) + "5ea4" + str(random.randint(0, 9)))
		frame.place(x=75, y=200)
		img = ImageTk.PhotoImage(Image.open(f"photo\\{id}.jpg").resize((300, 300)))   #Temporally using 00001.jpg for testing
		photo = tk.Label(frame, image= img)
		photo.image = img
		photo.pack()



if __name__ == "__main__":
    start = MainGUI()

"""
[X] Search bar
[ ] List
[ ] Options
[X] Refresh
"""