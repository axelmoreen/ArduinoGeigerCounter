import tkinter as tk
from CollectionWindow import CollectionWindow
import threading

import serial
global protocol


# collect.mainloop()
collecting = False
connected = False
counts = 0;

root = tk.Tk()
windows = []

collect = CollectionWindow(root)
windows.append(collect)

wthreads = [] * len(windows)

class SerialHandler(serial.LineReader):
    def connection_made(self, transport):
        super(SerialHandler, self).connection_made(transport)
        connected = True

    def handle_line(self, data):
        if (data.startsWith("COUNT")):
            parts = data.split(" ")
            time = int(parts[1])



def main():
    for i in range(0, windows):
        wthreads[i] = threading.Thread(target=windows[i].mainloop)
        wthreads[i].start()



    ser = serial.Serial("COM3", 9600)
    protocol = serial.ReaderThread(ser, SerialHandler)
    ser.open()

if __name__ == "__main__":
    main()