import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
data = logicData.LogicData(inFile, 'ms', 4)
data.set_decimal_points(10)
capture_data = data.get_raw_data()

rx = 0
tx = 0
last_sample = [0, 0]
last_ready_toggle = [0, 0]
for i in capture_data:
    ready = i[1] & 1
    ready_toggled = i[1] ^ last_sample[1] & 1
    disable_toggled = i[1] ^ last_sample[1] >> 1

    if disable_toggled:
        active_time = i[0] - last_ready_toggle[0]
        if last_ready_toggle[1] & 1:
            rx += active_time
        else:
            tx += active_time

    last_sample = i
    if ready_toggled:
        last_ready_toggle = i
radio_up_time = rx + tx

print("Radio usage: ", 100 * radio_up_time /capture_data[-1][0], "%")