import logicData
import sys

inFile = sys.argv[1]

data = logicData.LogicData(inFile, 'ms', 2)
data.set_decimal_points(2)
capture_data = data.get_raw_data()
ignore = 10

def ignore_tiny_toggles():
    ignore_sum = 0
    last_capture = [0, 0]
    for i in range(len(capture_data)-1):
        if (capture_data[i][0] - last_capture[0] < ignore) and capture_data[i][1] == 0 and not last_capture[1] & capture_data[i+1][1]:
            ignore_sum += capture_data[i][0] - last_capture[0]
        last_capture = capture_data[i]
    return ignore_sum

radio_up_time = 0
last_sample = [0, 0]
for i in capture_data:
    tx = i[1] & 1
    rx = i[1] >> 1
    if not i[1]:
        radio_up_time += i[0] - last_sample[0]
    last_sample = i

print("Radio usage: ", 100 * (radio_up_time + ignore_tiny_toggles())/capture_data[-1][0], "%")