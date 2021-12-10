from cgitb import text
from dataclasses import Field
from contact import *
import tkinter as tk
from PIL import Image, ImageTk

test1 = Contact("Hao", "492", "12345", "1mail", b'')
test2 = Contact("Thai", "987", "12345", "2mail", b'')
testList1 = [test1, test2, test1, test2, test1, test2]
testList2 = [test1, test2]

mainWindow = tk.Tk()


class InfoBar():
    def __init__(self, parrent, width, name: str, phone: str, mail: str, id: str) -> None:
        mainBar = tk.Frame(parrent, width=width, height=100, bg="red")
        mainBar.pack(padx=5, pady=5)
        self.width = width
        self.height = 100
        self.id = id

        #Labels
        self.name = tk.Label(mainBar, text="Name: " + name,
                             font=('Courier', 12), anchor=tk.W, bg="red")
        self.phone = tk.Label(mainBar, text="Number: " +
                              phone, font=('Courier', 12), anchor=tk.W, bg="red")
        self.mail = tk.Label(mainBar, text="Email: " + mail,
                             font=('Courier', 12), anchor=tk.W, bg="red")
        self.id = tk.Label(mainBar, text="ID: " + id,
                           font=('Courier', 12), anchor=tk.W, bg="red")

        #Pic holder
        self.picPlace = tk.Canvas(mainBar, bg= '#7e7e7e', width= 80, height= 80)
        img = ImageTk.PhotoImage(Image.open("photo\\00001.jpg").resize((80, 80)))   #Temporally using 00001.jpg for testing
        photo = tk.Label(self.picPlace, image= img)
        photo.image = img
        photo.pack()

        #Placement
        self.name.place(x=self.width / 3 + 10, y= self.height / 4, anchor= tk.W)
        self.id.place(x=self.width / 3 * 2 + 10, y=self.height / 4, anchor= tk.W)
        self.phone.place(x=self.width / 3 + 10, y=self.height / 4 * 2, anchor= tk.W)
        self.mail.place(x=self.width / 3 + 10, y=self.height / 4 * 3, anchor= tk.W)
        self.picPlace.place(x= self.width / 12, y= self.height / 2, anchor=tk.W)


class InfoBox():
    def __init__(self, parrent, width, x=0, y=0, lst: list = []) -> None:
        self.width = width
        self.lst = lst

        #Config
        self.container = tk.Frame(parrent)
        self.mainBox = tk.Canvas(self.container, width=width, height=480, bg="yellow")
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

        #main window
        mainWindow.title("Phone Book")
        mainWindow.geometry("1000x600")
        mainWindow.resizable(height=False, width=False)

        #Background
        mainCanvas = tk.Canvas(mainWindow,  width=1000,
                               height=600, bg="#007dfe")
        mainCanvas.pack()

        #Foreground
        inputFrame = tk.Frame(mainCanvas, bg="white")
        inputFrame.place(relwidth=0.95, relheight=0.95, relx=0.025, rely=0.025)

        #Phone book text
        phoneBookText = tk.Label(
            inputFrame, text='PHONE BOOK', font=("Courier", 40), bg="white")
        phoneBookText.pack()

        test = tk.Label(inputFrame, text="Testing",
                        font=("Courier", 13), bg="white")
        test.place(x=10, y=100)

        test = tk.Label(inputFrame, text="Testing",
                        font=("Courier", 13), bg="white")
        test.place(x=10, y=100)

        #Pic place holder
        frame = tk.Frame(inputFrame, width=200, height=200, bg="#7e7e7e")
        frame.place(x=100, y=350)

        #List Box
        self.listBox = InfoBox(inputFrame, 450, 470, 75)
        self.listBox.newList(testList1)
        self.listBox.refeshBox()

        #Test Button
        self.button = tk.Button(inputFrame, text= "Switch List", command= self.switchList)
        self.button.pack()

        mainWindow.mainloop()

    def switchList(self):
        self.lst = testList2
        self.listBox.newList(testList2)
        self.listBox.refeshBox()


if __name__ == "__main__":
    start = MainGUI()