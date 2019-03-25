from geiger.TimestampHistogram import TimestampHistogram
import sys

def printHelp():
    print("================================================================")
    print("GEN_HISTOGRAM.PY")
    print("================================================================")
    print("USAGE ")
    print("    gen_histogram.py [file]")
    print("")
    print("EXAMPLES")
    print("    gen_histogram.py cs-137-5cm.txt")
    print("")

def main():
    if len(sys.argv) < 2:
        printHelp()
        return

    h = TimestampHistogram(sample_length=5000, bin_size=1)

    file = sys.argv[1]
    n = 0
    started = False
    with open(file) as fp:
        line = fp.readline()

        while line:

            if "START" in line:
                started = True
                h.set_start(int(line.split(" ")[1]))
                #print("Started")

            if "END" in line:
                started = False
                #print("End")

            if (started):
                if "COUNT" in line:
                    #print("Count")
                    when = line.split(" ")[1]
                    h.plot(int(when))
                    n+=1

            line = fp.readline()
    print("Plotted %i points" % n)
    h.group_samples()

    h.display_histogram_and_fit_curve()

if __name__ == "__main__":
    main();