from TimestampHistogram import TimestampHistogram
import time
import random

h = TimestampHistogram(sample_length=500, bin_size=2)

h.set_start_now()
s = time.time() * 1000
t = 0
print("Generating random data")
while t < 90000:
    if random.random() > 0.9:
        h.plot(s + t)
    t += 1

h.group_samples()
h.display_histogram_and_fit_curve()