#importing the server class
import server
#Importing the client class
import client
#Importing the system modules for closing the application
import sys, os, signal
from threading import Thread
#Importing everything from the tkinter for the GUI 
from tkinter import *
#Importing messagebox module from the tkinter
from tkinter import messagebox

#ChatWindow Class
class ChatWindow:
    
    #Constructor
    def __init__(self):

        #Setting default ip and port for the client connection
        self.ip = "127.0.0.1"
        self.port = 55555

        #Create the window the object of Tkinter
        self.root = Tk()
        root = self.root

        #Hiding the window
        root.withdraw()

        #Setting is_client to False
        self.is_client = False
        txt = "Server"

        #Asking the user if he/she is a client or not
        if self.isClient():
            #Setting is_client to True
            self.is_client = True
            txt = "Client"

        #Initializing the socket
        self.initilizeSocket()

        #Unhide the GUI window
        root.deiconify()

        #Setting the Window Title
        self.root.title(f'SecureChat {txt}')
        self.root.config()
        #Setting the window width and height
        self.root.geometry('640x640')

        #Creating the container frame for the listbox and the scrollbar
        self.frame = Frame(root)

        #Creating the scrollbar and setting its position        
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        #Creating the Listbox and setting its position
        self.mylist = Listbox(self.frame, yscrollcommand = self.scrollbar.set )
        self.mylist.pack( side = TOP, fill = BOTH, expand = True )
        self.scrollbar.config( command = self.mylist.yview )

        #Setting frame positions
        self.frame.pack(side=TOP , fill = BOTH, expand=True)

        #Creating input message text field and setting its position
        self.textField = Entry(root)
        self.textField.pack(side = BOTTOM, fill = BOTH)

        #Creating label for the 'Enter Message'
        Label(root, text='Enter Message').pack(side = LEFT, fill = BOTH)

        #Creating Send button to send the message
        self.btn = Button(root, text="Send", command = self.sendMessage)
        self.btn.pack( side = RIGHT)

        #Setting window close event handler
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    #Method to show popup window for the ip and port input
    def getIpPort(self):
        #Create a Toplevel window or popup window
        top= Toplevel(self.root)
        #Setting its size and position
        top.geometry("200x80")

        #Making the window not to resizable
        top.resizable(False, False)
        #Disabling close button
        top.protocol("WM_DELETE_WINDOW", lambda: None)

        #Creating these variable to store the ip and port
        ipvar = StringVar()
        portvar = IntVar()

        #Setting default ip and port
        ipvar.set(self.ip)
        portvar.set(self.port)

        #Create an Entry Widget in the Toplevel window for the ip field
        Label(top, text='IP Address').grid(row = 0, column =0)
        self.ip_entry= Entry(top, textvariable=ipvar)
        self.ip_entry.grid(row = 0, column =1)

        #Creating an Entry Widget in the Toplevel window for the port field
        Label(top, text='Port').grid(row = 1, column =0)
        self.port_entry= Entry(top, textvariable=portvar)
        self.port_entry.grid(row = 1, column =1)

        #Create a Button to Connect to the server
        Button(top,text= "Connect", command=top.destroy).grid(row = 2, column =1)
        #Create a Button Widget to close the Toplevel Window
        button= Button(top, text="Close", command=self.close)
        button.grid(row = 2, column =0)

        #wait until connect button not pressed
        top.wait_window()
        
        return (ipvar.get(), portvar.get())

    #Method to show popup window for the ip and port input
    def isClient(self):
        #Create a Toplevel window or popup window
        top= Toplevel(self.root)
        #Setting its size and position
        top.geometry("220x60")

        #Making the window not to resizable
        top.resizable(False, False)
        #Disabling close button
        top.protocol("WM_DELETE_WINDOW", lambda: None)

        #Creating these variable to store the ip and port
        boolvar = BooleanVar()

        #Setting default ip and port
        boolvar.set(False)
        

        #Create an Entry Widget in the Toplevel window for the ip field
        Label(top, text='Are you a client or server').grid(row = 0, column =1, columnspan =3)

        #Create a Button to Connect to the server
        Button(top,text= "Client", command= lambda: (top.destroy(), boolvar.set(True),)).grid(row = 1, column =0)
        #Create a Button Widget to close the Toplevel Window
        Button(top, text="Server", command=lambda: (top.destroy(), boolvar.set(False),)).grid(row = 1, column =3)

        #wait until any button not pressed
        top.wait_window()
        
        return boolvar.get()

    #Method to call when server disconnected from the client
    def onserverdisconnect(self):
        print("Disconnected")
        if messagebox.askretrycancel("Connection Refused", "Disconnected, Try again?"):
            #If try again
            #Close the socket
            self.socket.close()
            #Again initialize the Socket
            self.initilizeSocket()
            #Start the socket
            self.connect()
        else:
            #Close the application
            self.close()

    #Method to call when cliet disconnected from the server
    def onclientdisconnect(self):
        print("Disconnected")
        messagebox.showinfo("Connection Close", "Client Disconnected")

    #Method to show that connection established
    def onconnect(self):
        messagebox.showinfo("Connection Established", "Connected Successfully")

    #Insert text to the listbox
    def insert(self, message, is_guest = True):
        txt=""
        if is_guest:
            txt = "Guest: "
        else:
            txt = "You: "
        #Inserting Text
        self.mylist.insert(END, txt+message)
        #Scrolling to the bottom
        self.mylist.yview_moveto(1)

    #Method to send message
    def sendMessage(self):
        #For Sending the message
        self.socket.send(self.textField.get())
        #Putting the message to the listbox
        self.insert(self.textField.get(), False)

    #Initializing the socket
    def initilizeSocket(self):
        if self.is_client:
            #If client
            #Getting the ip and port
            self.ip, self.port = self.getIpPort()
            #Initling the client socket
            self.socket = client.Client(ip = self.ip, port = self.port)
            #setting the disconnect callback method
            self.socket.setOnDisconnect(self.onserverdisconnect)
        else:
            #Initializing the server socket
            self.socket = server.Server()
            #setting th disconnect callback method
            self.socket.setOnDisconnect(self.onclientdisconnect)
        #setting connected callback method
        self.socket.setOnConnect(self.onconnect)

    #Method to start the sockets
    def connect(self):
        self.socket.setOnMessage(self.insert)
        Thread(target=self.socket.start).start()

    #Method to start the Application
    def start(self):
        self.connect()
        mainloop()

    #MEthod to close the Application
    def close(self):
        print("close")
        os.kill(os.getpid(), signal.SIGTERM)
        self.root.destroy()
        self.socket.close()

main = ChatWindow()
main.start()