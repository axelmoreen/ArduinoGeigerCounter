import tkinter as tk
from CollectionWindow import CollectionWindow
from ConnectionStatus import ConnectionStatus
from multiprocessing import Process, Event, Queue
from multiprocessing.managers import BaseManager

import time
import signal
import sys
import serial
import serial.threaded

global protocol
global updateThread
global serialThread

global ser

global status
global manager
global collectionStart




windows = []

window_types = [CollectionWindow]
wthreads = [None] * len(window_types)

def handle_exit():
    serialThread.terminate()
    updateThread.terminate()


def window_factory(_class):
    root = tk.Tk()
    window = _class(root)
    windows.append(window)
    window.mainloop()

class SerialThread(Process):
    def __init__(self, status, port="COM3", baudrate=9600, timeout=5):
        super(Process, self).__init__()

        self.status = status
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.collectionStart = 0
    def terminate(self):
        self.serial.close()


    def read_line(self, line):
        # print(line.strip())
        if line.startswith("START"):
            self.status.collecting = True
            self.collectionStart = time.time() * 1000

        if line.startswith("DURATION"):
            length = line.split(" ")[1]
            self.status.collection_duration = int(length)
        if line.startswith("END"):
            self.status.collecting = False

        if line.startswith("COUNT"):
            self.status.counts += 1

        self.status.time_elapsed = time.time() * 1000 - self.collectionStart

    def run(self):
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        time.sleep(1)
        self.write(bytes("COLLECT 30", "UTF-8"))
        self.read()

    def write(self, line):
        self.serial.write(line)
    def read(self):
        while self.serial.isOpen():
            self.status.connected = True
            line = self.serial.readline().decode()
            self.read_line(line)
        if not self.serial.isOpen():
            self.status.connected = False
            print("Serial is not opened.")

    def get_status(self):
        return self.status

class Timer(Process):
    def __init__(self, interval, function, args=[], kwargs={}):
        super(Timer, self).__init__()
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()

def main():
    global ser
    global status
    global manager
    signal.signal(signal.SIGINT, handle_exit)

    BaseManager.register('ConnectionStatus', ConnectionStatus)
    manager = BaseManager()
    manager.start()

    status = manager.ConnectionStatus()


    updateThread = Timer(1, update_window_information)
    updateThread.daemon = True
    updateThread.start()


    try:
        print("Opening serial connection.")
        serialThread = SerialThread(status,port="COM3", baudrate=9600, timeout=5)
        serialThread.daemon = True
        serialThread.start()
    except serial.SerialException as e:
        print("Error: ", e)
        connected = False

    for i in range(0, len(window_types)):
        wthreads[i] = Process(target=window_factory(window_types[i]), args=(window_types[i],))
        wthreads[i].start()
        wthreads[i].join()

        pass




def update_window_information():
    for window in windows:
        window.thread_queue.put(status)


if __name__ == "__main__":
    main()