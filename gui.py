import server
import client
import sys, os, signal
from threading import Thread
from tkinter import *
from tkinter import messagebox

class ChatWindow:
    def __init__(self):

        self.pid = os.getpid()

        self.root = Tk()
        root = self.root
        root.withdraw()

        self.is_client = False
        txt = "Server"

        if messagebox.askyesno("askyesno", "Are you a Client?"):
            self.is_client = True
            txt = "Client"

        self.initilizeSocket()

        root.deiconify()

        self.root.title(f'SecureChat {txt}')
        self.root.config()
        self.root.geometry('640x640')

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        
        self.mylist = Listbox(root, yscrollcommand = self.scrollbar.set )

        self.mylist.pack( side = TOP, fill = BOTH, expand = True )
        self.scrollbar.config( command = self.mylist.yview )

        self.e1 = Entry(root)
        self.e1.pack(side = BOTTOM, fill = BOTH)

        Label(root, text='Enter Message').pack(side = LEFT, fill = BOTH)

        self.btn = Button(root, text="Send", command = self.sendMessage)
        self.btn.pack( side = RIGHT)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def showPopup(self):
        #Create a Toplevel window
        top= Toplevel(self.root)
        top.geometry("200x80")

        ipvar = StringVar()
        portvar = IntVar()

        ipvar.set("127.0.0.1")
        portvar.set(55555)

        #Create an Entry Widget in the Toplevel window
        Label(top, text='IP Address').grid(row = 0, column =0)
        self.ip_entry= Entry(top, textvariable=ipvar)
        self.ip_entry.grid(row = 0, column =1)

        Label(top, text='Port').grid(row = 1, column =0)
        self.port_entry= Entry(top, textvariable=portvar)
        self.port_entry.grid(row = 1, column =1)

        #Create a Button to print something in the Entry widget
        Button(top,text= "Connect", command=top.destroy).grid(row = 2, column =1)
        #Create a Button Widget in the Toplevel Window
        button= Button(top, text="Close", command=self.close)
        button.grid(row = 2, column =0)

        top.wait_window()
        
        return (ipvar.get(), portvar.get())

    def ondisconnect(self):
        print("Disconnected")
        if messagebox.askretrycancel("Connection Refused", "Disconnected, Try again?"):
            self.socket.close()
            self.initilizeSocket()
            self.connect()
        else:
            self.close()

    def onconnect(self):
        messagebox.showinfo("Connection", "Connected Successfully")

    def insert(self, message, is_guest = True):
        txt=""
        if is_guest:
            txt = "Guest: "
        else:
            txt = "You: "
        self.mylist.insert(END, txt+message)
        self.mylist.yview_moveto(1)

    def sendMessage(self):
        self.socket.send(self.e1.get())
        self.insert(self.e1.get(), False)

    def initilizeSocket(self):
        if self.is_client:
            ip, port = self.showPopup()
            self.socket = client.Client(ip = ip, port = port)
            self.socket.setOnDisconnect(self.ondisconnect)
            self.socket.setOnConnect(self.onconnect)
        else:
            self.socket = server.Server()

    def connect(self):
        self.socket.setOnMessage(self.insert)
        Thread(target=self.socket.start).start()

    def start(self):
        self.connect()
        mainloop()

    def close(self):
        print("close")
        os.kill(os.getpid(), signal.SIGTERM)
        self.root.destroy()
        self.socket.close()

main = ChatWindow()
main.start()