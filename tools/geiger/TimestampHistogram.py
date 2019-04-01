import time
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

text_vheight = 0.8
margin = -2
class TimestampHistogram:
    def __init__(self, sample_length=5000, bin_size=20):
        self.sample_length = sample_length
        self.samples = []
        self.points = []
        self.bin_size = bin_size
        self.set_start_now()

    def flush_data(self):
        self.points.clear()
        self.samples.clear()
        self.set_start_now()

    def set_start_now(self):
        self.start = time.time() * 1000

    def plot_now(self):
        self.points.append(time.time() * 1000)

    def set_start(self, timestamp):
        self.start = timestamp

    def plot(self, timestamp):
        self.points.append(timestamp)

    def group_samples(self):
        self.samples.clear()
        maxtime = np.amax(self.points) - self.start;
        n_groups = math.ceil(maxtime/self.sample_length)
        print("Num groups ",n_groups)
        self.samples = [[] for i in range(n_groups)]
        for p in self.points:
            group = math.floor((p - self.start) / self.sample_length)
            self.samples[group].append(p)

    def display_histogram_and_fit_curve(self):
        countrate = []
        total = 0
        num_g = 0
        for i in range(0, len(self.samples)):
            group = self.samples[i]
            if not group: continue
            if (len(group) == 0):
                continue

            countrate.append(len(group))
            total += len(group)
            num_g += 1

        print("Sampled counts: ")
        print(countrate)
        self.bin_start = self.bin_size * int(round(np.amin(countrate) / self.bin_size))

        n = self.bin_start
        bin_array = []
        bin_max = self.bin_start
        while n < np.amax(countrate):
            bin_array.append(n)
            n += self.bin_size
            bin_max = n

        print(self.bin_start, bin_array)
        out = plt.hist(countrate, bins=bin_array, edgecolor='black', linewidth='0.8')
        plt.title('Histogram of Counts')
        plt.xlabel('Counts (counts)')
        plt.ylabel('Frequency')



        print("Histogram output: ")
        print(out)

        centers = out[1][:-1] + np.diff(out[1]) /2

        n = len(centers)
        # mean = sum(centers * out[0]) / n
        mean = total / num_g
        sigma = sum(out[0] * (centers - mean) ** 2) / n
        print("Mean: ", mean, ", Sigma: ", sigma)
        print("Centers")
        print(centers)

        param, pcov = curve_fit(gaussian_function, centers, out[0], p0=[1, mean, sigma, 1])
        print("A * exp(-(x-b)^2/C^2)+D")
        print(param)

        x = np.linspace(self.bin_start, bin_max, 100)
        y = gaussian_function(x, param[0], param[1], param[2], param[3])
        ymax = np.amax(out[0])
        #plt.text(bin_max - margin, ymax, "Curve Fit:")
        #plt.text(bin_max - margin, ymax - text_vheight, "A * exp(-(x-b)^2/C^2)+D")
        #plt.text(bin_max - margin, ymax - (2 * text_vheight), "A=%3.f" % param[0] + ", B=%3.f" % param[1] + ", C=%3.f" % param[2] + ", D=%3.f" % param[3])

        #error = np.sqrt(np.diag(pcov))
        #print(error)

        #plt.text(bin_max - margin, ymax - (3 * text_vheight), "σ=" + np.array2string(error, precision=3))

        plt.plot(x,y)
        plt.show()
        print("Graphed data")

# A * exp(-(x-b)^2/C^2)+D
def gaussian_function(x, a, b, c, d):
    return a * np.exp(-((x-b)**2)/(c**2))+d