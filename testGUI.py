from cgitb import text
from dataclasses import Field
from tkinter.constants import LEFT, Y
from contact import *
import tkinter as tk
from PIL import Image, ImageTk

test1 = Contact("Hao", "492", "12345", "1mail", b'')
test2 = Contact("Thai", "987", "12345", "2mail", b'')
test3 = Contact("Thai", "987", "12345", "2mail", b'')
test4 = Contact("Thai", "987", "12345", "2mail", b'')
test5 = Contact("Thai", "987", "12345", "2mail", b'')
test6 = Contact("Thai", "987", "12345", "2mail", b'')
testList = [test1, test2, test3, test4, test5, test6]

mainWindow = tk.Tk()
mainWindow.wm_attributes('-transparentcolor', 'purple')


class InfoBar():
    def __init__(self, parrent, width, name: str, phone: str, mail: str, id: str) -> None:
        mainBar = tk.Frame(parrent, width=width - 10, height=100, bg="red")
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
        img = ImageTk.PhotoImage(Image.open("photo\\00001.jpg").resize((80, 80)))
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

        #Config
        self.container = tk.Frame(parrent)
        self.mainBox = tk.Canvas(self.container, width=width, height=480, bg="yellow")

        self.scrol = tk.Scrollbar(self.container, command= self.mainBox.yview)
        self.scrollableFrame = tk.Frame(self.mainBox)

        self.scrollableFrame.bind("<Configure>", lambda e: self.mainBox.configure(scrollregion=self.mainBox.bbox("all")))

        self.mainBox.create_window((0, 0), window= self.scrollableFrame, anchor= tk.NW)
        self.mainBox.config(yscrollcommand= self.scrol.set)

        #Placement
        self.container.place(x=x, y=y)
        self.mainBox.pack(side= tk.LEFT, fill= tk.BOTH, expand= True)
        self.scrol.pack(side = tk.RIGHT, fill= Y)
        
        for contact in lst:
            self.createBar(contact)

    def createBar(self, contact: Contact):
        newBar = InfoBar(self.scrollableFrame, self.width - 10, contact.getName(),
                         contact.getPhone(), contact.getEmail(), contact.getID())


class MainGUI():
    def __init__(self) -> None:
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

        testbox = InfoBox(inputFrame, 450, 480, 75, testList)

        mainWindow.mainloop()


start = MainGUI()

# from tkinter import *   # from x import * is bad practice

# # http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

# class VerticalScrolledFrame(Frame):
#     """A pure Tkinter scrollable frame that actually works!
#     * Use the 'interior' attribute to place widgets inside the scrollable frame
#     * Construct and pack/place/grid normally
#     * This frame only allows vertical scrolling

#     """
#     def __init__(self, parent, *args, **kw):
#         Frame.__init__(self, parent, *args, **kw)            

#         # create a canvas object and a vertical scrollbar for scrolling it
#         vscrollbar = Scrollbar(self, orient=VERTICAL)
#         vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
#         canvas = Canvas(self, bd=0, highlightthickness=0,
#                         yscrollcommand=vscrollbar.set)
#         canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
#         vscrollbar.config(command=canvas.yview)

#         # reset the view
#         canvas.xview_moveto(0)
#         canvas.yview_moveto(0)

#         # create a frame inside the canvas which will be scrolled with it
#         self.interior = interior = Frame(canvas)
#         interior_id = canvas.create_window(0, 0, window=interior,
#                                            anchor=NW)

#         # track changes to the canvas and frame width and sync them,
#         # also updating the scrollbar
#         def _configure_interior(event):
#             # update the scrollbars to match the size of the inner frame
#             size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
#             canvas.config(scrollregion="0 0 %s %s" % size)
#             if interior.winfo_reqwidth() != canvas.winfo_width():
#                 # update the canvas's width to fit the inner frame
#                 canvas.config(width=interior.winfo_reqwidth())
#         interior.bind('<Configure>', _configure_interior)

#         def _configure_canvas(event):
#             if interior.winfo_reqwidth() != canvas.winfo_width():
#                 # update the inner frame's width to fill the canvas
#                 canvas.itemconfigure(interior_id, width=canvas.winfo_width())
#         canvas.bind('<Configure>', _configure_canvas)


# if __name__ == "__main__":

#     class SampleApp(Tk):
#         def __init__(self, *args, **kwargs):
#             root = Tk.__init__(self, *args, **kwargs)


#             self.frame = VerticalScrolledFrame(root)
#             self.frame.pack()
#             self.label = Label(text="Shrink the window to activate the scrollbar.")
#             self.label.pack()
#             buttons = []
#             for i in range(10):
#                 buttons.append(Button(self.frame.interior, text="Button " + str(i)))
#                 buttons[-1].pack()

#     app = SampleApp()
#     app.mainloop()