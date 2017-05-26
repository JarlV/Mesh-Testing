# For every 'disable' toggle, the time since last 'ready' toggle is considered
# active time for the radio. If the pin for 'ready' is HIGH at the time of the
# 'disable' toggle, the radio is considered to be in Rx mode since the time of the
# 'ready' pin toggle. Otherwise, the radio is considered to be in Tx mode since the
# time of the 'ready' pin toggle.

import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
data = logicData.LogicData(inFile, 'ms', 2)
data.set_decimal_points(2)
capture_data = data.get_raw_data()

first_ready_toggle = 0
rx = 0
tx = 0
last_sample = capture_data[0]
last_ready_toggle = 0
for i in range(1, len(capture_data)):
    ready = capture_data[i][1] & 1
    ready_toggled = (capture_data[i][1] ^ last_sample[1]) & 1
    disable_toggled = (capture_data[i][1] ^ last_sample[1]) >> 1

    if disable_toggled and first_ready_toggle and capture_data[i][0] - last_sample[0] > 0.001:
        active_time = capture_data[i][0] - last_ready_toggle[0]
        if ready:
            rx += active_time
        else:
            tx += active_time
    elif ready_toggled:
        first_ready_toggle = 1
        last_ready_toggle = capture_data[i]
    last_sample = capture_data[i]

print("Radio usage (Tx): ", 100 * tx / capture_data[-1][0], "%")
print("Radio usage (Rx): ", 100 * rx / capture_data[-1][0], "%")

#  Graphics
labels = ['Scanning', 'Transmitting', 'Idle']
sizes = [rx, tx, capture_data[-1][0] - rx + tx]
colors = ['lightgreen', 'lightskyblue', 'Lightgray']
plt.pie(sizes, colors=colors, labels=labels, startangle=90, autopct='%1.'+ str(data.decimal_points) +'f%%')
plt.axis('equal')
plt.tight_layout()
plt.show()