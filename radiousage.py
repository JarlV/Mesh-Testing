#  Test for calculating the amount of time in in which the radio is active / total time.
#  Run the test in console with .csv file exported from Saleae Logic device as argument.
#  The .csv file would have been exported from a capture of channels 0 and 1, where 'high line' meaning 'radio active'.

import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
data = logicData.LogicData(inFile, 'ms', 2)
data.set_decimal_points(2)
capture_data = data.get_raw_data()
ignore = 10

def ignore_tiny_toggles():
    ignore_sum = 0
    last_capture = [0, 0]
    for i in range(len(capture_data)-1):
        if (capture_data[i][0] - last_capture[0] < ignore) \
                and capture_data[i][1] == 0 and not last_capture[1] & capture_data[i+1][1]:
            ignore_sum += capture_data[i][0] - last_capture[0]
        last_capture = capture_data[i]
    return ignore_sum

radio_up_time = 0
rx = 0
tx = 0
last_sample = [0, 0]
for i in capture_data:
    if i[1] == 0b01:
        tx += i[0] - last_sample[0]
    elif i[1] == 0b10:
        rx += i[0] - last_sample[0]
        #radio_up_time += i[0] - last_sample[0]
    last_sample = i
radio_up_time = rx + tx

print("Radio usage: ", 100 * (radio_up_time + ignore_tiny_toggles())/capture_data[-1][0], "%")
rx += ignore_tiny_toggles()


labels = ['Scanning', 'Transmitting', 'Idle']
sizes = [rx, tx]
colors = ['gold', 'lightskyblue', 'black']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()