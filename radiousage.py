#  Test for calculating the amount of time in in which the radio is active / total time.
#  Run the test in console with .csv file exported from Saleae Logic device as argument.
#  The .csv file would have been exported from a capture of channels 0 and 1, where 'high line' meaning 'radio active'.

import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
data = logicData.LogicData(inFile, 'ms', 4)
data.set_decimal_points(2)
capture_data = data.get_raw_data()
ignore = 1

def ignore_tiny_toggles():
    sum = 0
    last_capture = [0, 0]
    for i in range(len(capture_data)):
        if capture_data[i][1] >> 1 and capture_data[i][0] - last_capture[0] < ignore:  # and last_capture[1] >> 1 == 0:
            sum += capture_data[i][0] - last_capture[0]
        last_capture = capture_data[i]
    return sum

rx = 0
tx = 0
last_sample = [0, 0]
for i in capture_data:
    if last_sample[1] & 1:
        tx += i[0] - last_sample[0]
    elif last_sample[1] >> 1:
        rx += i[0] - last_sample[0]
    last_sample = i
rx += ignore_tiny_toggles()
radio_up_time = rx + tx

print("Radio usage: ", 100 * radio_up_time /capture_data[-1][0], "%")

#  Graphics
labels = ['Scanning', 'Transmitting', 'Idle']
sizes = [rx, tx, capture_data[-1][0] - rx + tx]
colors = ['gold', 'lightskyblue', 'lightgreen']
plt.pie(sizes, colors=colors, labels=labels, startangle=90, autopct='%1.2f%%')
plt.axis('equal')
plt.tight_layout()
plt.show()