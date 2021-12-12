#from _typeshed import Self         #<<< Báo lỗi nên tạm thời vô hiệu hóa
from cgitb import text
from time import sleep
from tkinter.font import Font
from contact import *
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
import socket
import pickle

# region Socket
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

COMMAND = {							#<<<<<< COMMAND 'FIND' sẽ đính kèm theo thông tin cần tìm ở đằng sau nhe. VD: !FIND_NAME_Hao
    0: "!DISCONNECT",
    1: "!DISPLAY_LIST",
    2: "!FIND_NAME_",
    3: "!FIND_NUMB_",
    4: "!FIND_MAIL_"
}

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectSocket():
    notCnnt = True
    while notCnnt:
        try:
            serverSocket.connect(ADDR)
            notCnnt = False
            _msg = tk.Label(inputFrame, text="Connected!", font=("Arial", 10), bg=LightGrey)
            _msg.place(x=883, y=40)
        except socket.error as msg:
            _warn = tk.Label(inputFrame, text="Already connected!", font=("Arial", 10), bg=LightGrey)
            _warn.place(x=837, y=40)
            print(msg)
            break


def closeSocket():
	try:
		serverSocket.send(COMMAND[0].encode(FORMAT))
	except:
		pass
	serverSocket.close()

# endregion

# region Color
Grey = "#E8E8E8"
LightGrey = "#f0f0f0"
Navy = "#14279B"
Bluely = "#3D56B2"
SkyBlue = "#5C7AEA"
# endregion

# region Testing
test1 = Contact("Hao", "00001", "12345", "1mail", b'')
test2 = Contact("Thai", "00002", "12345", "2mail", b'')
testList1 = [test1, test2, test1, test2, test1, test2]
testList2 = [test1, test2]
# endregion

# closing window
def onClose():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		mainWindow.destroy()
		closeSocket()

# region Main window
mainWindow = tk.Tk()
mainWindow.title("FoneBook")
mainWindow.geometry("1000x600")
mainWindow.resizable(height=False, width=False)
mainWindow.protocol("WM_DELETE_WINDOW", onClose)

# Background
mainCanvas = tk.Canvas(mainWindow,  width=1000,
                       height=600, bg=Bluely)
mainCanvas.pack()

# Foreground
inputFrame = tk.Frame(mainCanvas, bg=LightGrey)
inputFrame.place(relwidth=0.96, relheight=0.94, relx=0.02, rely=0.03)
# endregion

def sendAndRecv(msg: str) -> list:							#<<<<<<<<<<<<< Sử dụng hàm này kết hợp với các COMMAND đã được định sẵn ở trên để làm tiếp nhe
	sendingMsg = msg.encode(FORMAT)							# Dữ liệu return sẽ luôn là []/list á
	serverSocket.send(sendingMsg)

	recvmsgLen = serverSocket.recv(SIZE).decode(FORMAT)
	recvmsg = serverSocket.recv(int(recvmsgLen))
	result = pickle.loads(recvmsg)

	return result

class InfoBar():
    def __init__(self, parrent, width, name: str, phone: str, mail: str, id: str) -> None:
        mainBar = tk.Frame(parrent, width=width, height=100, bg=Grey)
        mainBar.pack(padx=5, pady=5)
        self.width = width
        self.height = 100
        self.id = id

    # Labels
        self.name = tk.Label(mainBar, text="Name: " + name,
                             font=('Arial Bold', 12), anchor=tk.W, bg=Grey, fg="black")
        self.phone = tk.Label(mainBar, text="Number: " +
                              phone, font=('Arial', 12), anchor=tk.W, bg=Grey, fg="black")
        self.mail = tk.Label(mainBar, text="Email: " + mail,
                             font=('Arial', 12), anchor=tk.W, bg=Grey, fg="black")
        self.id = tk.Label(mainBar, text="ID: " + id,
                           font=('Arial Italic', 12), anchor=tk.W, bg=Grey, fg="black")

    # Button "View Avatar"
        avaBttn = tk.Button(mainBar, text="View Avatar", anchor=tk.W,
                            command=lambda: MainGUI.ViewAva(id), bg=Bluely, fg="white")

    # Pic holder
        self.picPlace = tk.Canvas(mainBar, bg='#7e7e7e', width=80, height=80)
        img = ImageTk.PhotoImage(Image.open(f"client\\{id}.jpg").resize(
            (80, 80)))  # Temporally using 00001.jpg for testing
        photo = tk.Label(self.picPlace, image=img)
        photo.image = img
        photo.pack()

        # Placement
        self.name.place(x=self.width / 3 - 20, y=self.height / 4, anchor=tk.W)
        self.id.place(x=self.width - 80, y=self.height / 4, anchor=tk.W)
        self.phone.place(x=self.width / 3 - 20,
                         y=self.height / 4 * 2, anchor=tk.W)
        self.mail.place(x=self.width / 3 - 20,
                        y=self.height / 4 * 3, anchor=tk.W)
        avaBttn.place(x=self.width - 80, y=self.height - 20, anchor=tk.W)
        self.picPlace.place(x=self.width / 12, y=self.height / 2, anchor=tk.W)


class InfoBox():
	def __init__(self, parrent, width, x=0, y=0, lst: list = []) -> None:
		self.width = width
		self.lst = lst

		# Config
		self.container = tk.Frame(parrent)
		self.mainBox = tk.Canvas(
			self.container, width=width, height=480, bg=LightGrey)
		self.mainBox.pack_propagate(0)

		self.scrol = tk.Scrollbar(self.container, command=self.mainBox.yview)
		self.scrollableFrame = tk.Frame(self.mainBox)

		self.scrollableFrame.bind("<Configure>", lambda e: self.mainBox.configure(
			scrollregion=self.mainBox.bbox("all")))

		self.mainBox.create_window(
			(0, 0), window=self.scrollableFrame, anchor=tk.NW)
		self.mainBox.config(yscrollcommand=self.scrol.set)

		# FRAME  ->  CANVAS  ->  FRAME
		#  ^          ^           ^
		# Attach    Restrict     Scrollable
		# Scrollbar  the field

		# Placement
		self.container.place(x=x, y=y)
		self.mainBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.scrol.pack(side=tk.RIGHT, fill=tk.Y)

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

        self.lst = None

        # Phone book text
        phoneBookText = tk.Label(inputFrame, text='fonebook', font=(
            "Arial Black", 40), fg=Bluely, bg=LightGrey)
        phoneBookText.place(x=30, y=5)

        credit = tk.Label(inputFrame, text="by Team 10, not Mark",
                            font=("Comic Sans MS", 12), fg=Navy, bg=LightGrey)
        credit.place(x=300, y=45)

        # List Box
        self.listBox = InfoBox(inputFrame, 450, 470, 75)

        # Refresh Button
        #refreshbttn = tk.Button(inputFrame, text="Refresh",
        #                        command=self.listBox.refeshBox)
        #refreshbttn.place(x=900, y=10)

        # Connect Button
        connectbttn = tk.Button(
            inputFrame, text="Connect", bg=Bluely, fg="white", command=connectSocket)
        connectbttn.place(x=895, y=10)

        # Display button
        displaybttn = tk.Button(
            inputFrame, text="Display All", bg=Bluely, fg="white", command= self.displayList)
        displaybttn.place(x=680, y=45)

        # Search bar (Name)
        # Label
        srcNameLabel = tk.Label(
            inputFrame, text="Name", font=("Arial", 11), bg=LightGrey, fg="black"
        )
        srcNameLabel.place(x=34, y=90)

        # Bar
        srcNameBox = tk.Entry(
            inputFrame,  width=44
        )
        srcNameBox.place(x=36, y=116)

        # Button
        srcNameBttn = tk.Button(
            inputFrame, text="Search", bg=Bluely, fg="white", command=lambda:MainGUI.searchName(self, srcNameBox.get())
        )
        srcNameBttn.place(x=310, y=113)

        # Search bar (phone number)
        # Label
        srcNumLabel = tk.Label(
            inputFrame, text="Phone number", font=("Arial", 11), bg=LightGrey, fg="black"
        )
        srcNumLabel.place(x=34, y=140)

        # Bar
        srcNumBox = tk.Entry(
            inputFrame,  width=44
        )
        srcNumBox.place(x=36, y=166)

        # Button
        srcNumBttn = tk.Button(
            inputFrame, text="Search", bg=Bluely, fg="white", command=lambda:MainGUI.searchNum(self, srcNumBox.get())
        )
        srcNumBttn.place(x=310, y=163)

        # Search bar (email)
        # Label
        srcEmailLabel = tk.Label(
            inputFrame, text="Email", font=("Arial", 11), bg=LightGrey, fg="black"
        )
        srcEmailLabel.place(x=34, y=190)

        # Bar
        srcEmailBox = tk.Entry(
            inputFrame,  width=44
        )
        srcEmailBox.place(x=36, y=216)

        # Button
        srcEmailBttn = tk.Button(
            inputFrame, text="Search", bg=Bluely, fg="white", command=lambda:MainGUI.searchEmail(self, srcEmailBox.get())
        )
        srcEmailBttn.place(x=310, y=213)

        mainWindow.mainloop()

    def displayList(self):
        self.lst = sendAndRecv(COMMAND[1])
        self.listBox.newList(self.lst)
        self.listBox.refeshBox()

    def searchName(self, name: str):
        self.lst = sendAndRecv(COMMAND[2]+name)
        self.listBox.newList(self.lst)
        self.listBox.refeshBox()

    def searchNum(self, num: str):
        self.lst = sendAndRecv(COMMAND[3]+num)
        self.listBox.newList(self.lst)
        self.listBox.refeshBox()

    def searchEmail(self, email: str):
        self.lst = sendAndRecv(COMMAND[4]+email)
        self.listBox.newList(self.lst)
        self.listBox.refeshBox()

    def ViewAva(id: str):
        frame = tk.Frame(inputFrame, width=267, height=267, bg="#000000")
        frame.place(x=34, y=260)
        img = ImageTk.PhotoImage(Image.open(f"photo\\{id}.jpg").resize(
            (267, 267)))  # Temporally using 00001.jpg for testing
        photo = tk.Label(frame, image=img)
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
