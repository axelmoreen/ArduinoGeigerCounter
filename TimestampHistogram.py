import time
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class TimestampHistogram:
    def __init__(self, sample_length=5000, bin_size=20, bin_start=0):
        self.sample_length = sample_length
        self.samples = []
        self.points = []
        self.bin_size = bin_size
        self.bin_start = bin_start
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
        for p in self.points:
            group = math.floor((p - self.start) / self.sample_length)
            if not group in self.samples:
                self.samples.append([])
            # print(str(p) +", "+str(group))
            # print(self.samples[group])
            (self.samples[group]).append(p)
            # print(len(self.samples[group]))

    def display_histogram_and_fit_curve(self):
        countrate = []
        for group in self.samples:
            if (len(group) == 0):
                continue
            # print(group)
            # print("Length: " +str(len(group)))
            countrate.append(1000 * len(group) / self.sample_length )
        print("Sampled count rates: ")
        print(countrate)
        n = self.bin_start
        bin_array = []
        bin_max = self.bin_start
        while n < np.amax(countrate):
            bin_array.append(n)
            n += self.bin_size
            bin_max = n

        out = plt.hist(countrate, bins=bin_array, edgecolor='black', linewidth='0.8')
        plt.title('Histogram of Counts')
        plt.xlabel('Count Rate (counts/second)')
        plt.ylabel('Frequency')



        print("Histogram output: ")
        print(out)

        centers = out[1][:-1] + np.diff(out[1]) /2

        n = len(centers)  # the number of data
        mean = sum(centers * out[0]) / n  # note this correction
        sigma = sum(out[0] * (centers - mean) ** 2) / n  # note this correction

        print("Centers")
        print(centers)
        param, popt = curve_fit(gaussian_function, centers, out[0], p0=[1, mean, sigma, 1])
        print("A * exp(-(x-b)^2/C^2)+D")
        print(param)

        x = np.linspace(self.bin_start, bin_max, 100)
        y = gaussian_function(x, param[0], param[1], param[2], param[3])

        plt.plot(x,y)
        plt.show()
        print("Graphed data")

# A * exp(-(x-b)^2/C^2)+D
def gaussian_function(x, a, b, c, d):
    return a * np.exp(-((x-b)**2)/(c**2))+d