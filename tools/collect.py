import sys
import serial
import time



def printHelp():
    print("================================================================")
    print("COLLECT.PY")
    print("================================================================")
    print("USAGE ")
    print("    collect.py [outputfile] --time=[sec]")
    print("")
    print("OPTIONS")
    print("-t, --time    Amount of time to collect data, in seconds. If zero, collect indefinitely.")
    print("")
    print("EXAMPLES")
    print("    collect.py cs-137-5cm.txt --time=20")
    print("")

def main():
    out = ""
    if len(sys.argv) < 2:
        printHelp()
        return

    outfile = sys.argv[1]
    timestring = sys.argv[2]
    length = timestring.split("=")[1]
    try:
        ser = serial.Serial(port="COM3", baudrate=9600, timeout=5)
        time.sleep(3)
        print("Connected")
        ser.write(bytes("COLLECT " + length, "UTF-8"))
        while ser.isOpen():
            line = ser.readline().decode("UTF-8", errors="ignore").strip()
            out += line + "\n"
            print(line)
            if "END" in line:
                ser.close()
                break

        with open(outfile, 'w') as file:
            file.write(out)
        print("Collection complete")
    except serial.SerialException:
        print("Could not connect")







if __name__ == "__main__":
    main()