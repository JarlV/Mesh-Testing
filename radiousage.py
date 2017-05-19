import logicData
import sys

inFile = sys.argv[1]

data = logicData.LogicData(inFile, 'ms', 2)
data.set_decimal_points(2)
capture_data = data.get_raw_data()
ignore = 50


def ignore_tiny_toggles():
    for i in capture_data:
        

radio_up_time = 0
last_sample = [0, 0]
for i in capture_data:
    tx = i[1] & 1
    rx = i[1] >> 1
    if tx | rx:
        radio_up_time += i[0] - last_sample[0]
    last_sample = i

print()