from tkinter import *
import tkinter as tk
import queue
from ConnectionStatus import ConnectionStatus

global connection
connection = ConnectionStatus()

class CollectionWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.thread_queue = queue.Queue()
        master.title("Geiger Counter Collection")

        self.go = CollectionGo(self)
        self.diagnostic = CollectionDiagnostic(self)

        self.update_window_type()

        self.pack(padx=10, pady=10)
    def update_window_type(self):
        if connection.collecting:
            self.go.pack_forget()
            self.diagnostic.pack()

        else:
            self.diagnostic.pack_forget()
            self.go.pack()
    def update_status(self):
        try:
            while self.thread_queue.qsize():
                self.res = self.thread_queue.get(0)
                connection = self.res
        except queue.Empty:
            pass
        finally:
            self.master.after(100, self.update_status)



class CollectionGo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        text = "Connect to a device to begin collection."
        c = connection.connected
        if c:
            text = "Connected on "+connection.connection_string
        self.collectionString = Label(self, text=text);
        self.collectionString.grid(row = 0, columnspan=2, pady=(0,20))
        c = connection.connected
        self.collectionAmountString = Label(self, text="Collection Length");
        if c:
            self.collectionAmountString.grid(row=1, columnspan=2)
        self.collectionAmount = Entry(self)
        self.collectionUnits = Label(self, text="seconds")
        if c:
            self.collectionAmount.grid(row=2, column=0)
            self.collectionUnits.grid(row=2, column=1)

        state = DISABLED
        if c:
            state=ACTIVE
        self.collectionGo = Button(self, text="Start Collection", state=state)

        self.collectionGo.grid(row=3, columnspan=2, pady=10)

class CollectionDiagnostic(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.connectedString = Label(self, text="Collecting on "+connection.connection_string)
        self.connectedString.grid(row=0, pady=(0,25))

        self.elapsedString = Label(self, text="Elapsed: %i seconds" % connection.time_elapsed)
        self.elapsedString.grid(row=1)

        self.durationString = Label(self, text="Duration: %i seconds" % connection.collection_duration)
        self.durationString.grid(row=2)
        avg = 0
        if connection.time_elapsed > 0:
            avg = connection.counts / connection.time_elapsed

        self.averageString = Label(self, text="Average rate: %.2f counts/sec" % avg)
        self.averageString.grid(row=3, pady=(10, 0))


        self.collectionStop = Button(self, text="Stop Collection", state= ACTIVE)
        self.collectionStop.grid(row=4, pady=10)




