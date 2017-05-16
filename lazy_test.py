# Run test:
# lazy_test.py <.csv capture data>

import logicData
import sys

inFile = sys.argv[1]
outFile = "output/"

scanner_lazy = []
transmit_lazy = []
transmit_delta_times = []

data = logicData.LogicData(inFile, "ms", 8)
data.set_decimal_points(2)
capture_data = data.get_raw_data()

last_sample = 0
for i in capture_data:
    current_transmit_lazy = i[1] & 0b111
    current_transmit_timeout = ((i[1] >> 3) & 1) ^ ((last_sample >> 3) & 1)
    current_scanning_lazy = (i[1] >> 4) & 0b111
    current_scanning_timeout = (i[1] >> 7) ^ (last_sample >> 7)
    if current_scanning_timeout:  # if current_timeout is scanner timeout
        scanner_lazy.append([i[0],current_scanning_lazy])
    elif current_transmit_timeout:  # if current_timeout is transmit timeout
        transmit_lazy.append([i[0], current_transmit_lazy])
        transmit_delta_times.append(i[0])
    last_sample = i[1]

def validate_intervals(data, imin, imax):
    interval = imin
    fail_count = 0
    for time in data:
        if interval/2 <= time < interval:
            pass
        elif imin/2 <= time < imin:
            interval = imin
        else:
            print("     test fail on", time, "for interval", interval)
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax
    print("Amount of anomalies in intervals: ", fail_count, "out of", len(transmit_delta_times), "total.")

validate_intervals(logicData.get_delta_times(transmit_delta_times),
                   100,
                   2000)

logicData.save(scanner_lazy, outFile + 'scanner_lazy.csv')
logicData.save(transmit_lazy, outFile + 'transmit_lazy.csv')

