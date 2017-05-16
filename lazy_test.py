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

# Trickle test -------------------------------

imin = 100
imax = 2000

def validate_trickle(data,imin,imax):
    interval = imin
    last_interval = 0
    fail_count = 0
    for time in data:
        if interval/2 <= time < interval + last_interval/2:
            pass
        elif imin/2 <= time < imin + last_interval/2:
            interval = imin
        else:
            print("     test fail on", time, "for interval", interval)
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax
        last_interval = interval
    print("Amount of anomalies in intervals: ", fail_count, "out of", len(transmit_delta_times), "total.")   

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

validate_trickle(logicData.get_delta_times(transmit_delta_times),
                   imin,
                   imax)

trickle_out_data = [[i] for i in logicData.get_delta_times(transmit_delta_times)]
trickle_min_vals = [imin/2]
trickle_max_vals = [imin-1]
next_min = imin/2
next_max = imin-1
last_i = 0
for i in range(len(trickle_out_data)):
    if next_max*2 < imax:
        next_max *= 2
        trickle_max_vals.append(next_max + last_i/2)
    else:
        trickle_max_vals.append(imax-1 + last_i/2)
    last_i = next_max
    if next_min*2 < imax/2:
        next_min *= 2
        trickle_min_vals.append(next_min)
    else:
        trickle_min_vals.append(imax/2)

print(len(trickle_out_data), len(trickle_min_vals), len(trickle_max_vals))

for i in range(len(trickle_out_data)):
    trickle_out_data[i] = trickle_out_data[i] + [trickle_min_vals[i]] + [trickle_max_vals[i]]


logicData.save(trickle_out_data, outFile + 'trickle.csv')
logicData.save(scanner_lazy, outFile + 'scanner_lazy.csv')
logicData.save(transmit_lazy, outFile + 'transmit_lazy.csv')

