# Run test:
# lazy_test.py <.csv capture data>

import trickle
import logicData
import sys

inFile = sys.argv[1]
outFile = "output/"

scanner_lazy = []
transmit_lazy = []

data = logicData.LogicData(inFile, "ms", 8)
data.set_decimal_points(2)
capture_data = data.get_raw_data()
transmit_delta_times = [capture_data[0][0]]

i_toggles = []
t_toggles = []

last_sample = 0
for i in capture_data:
    current_transmit_lazy = i[1] & 0b111
    current_transmit_timeout = ((i[1] >> 3) & 1) ^ ((last_sample >> 3) & 1)
    current_scanning_lazy = (i[1] >> 4) & 0b111
    current_scanning_timeout = (i[1] >> 7) ^ (last_sample >> 7)
    if current_scanning_timeout:  # if scanner timeout
        scanner_lazy.append([i[0],current_scanning_lazy])
    elif current_transmit_timeout:  # if transmit timeout
        transmit_lazy.append([i[0], current_transmit_lazy])
        transmit_delta_times.append(i[0])
    if (i[1] >> 7) & 1 is not (last_sample >> 7) & 1:
        i_toggles.append(i[0])
    if i[1] >> 8 is not last_sample >> 8:
        t_toggles.append(i[10])
    last_sample = i[1]

# Trickle test -------------------------------

imin = 100
imax = 2000


trickle_out_data = \
    trickle.determine_min_max(imin,
                              imax,
                              logicData.get_delta_times(transmit_delta_times))


logicData.save(trickle_out_data, outFile + 'trickle.csv')
logicData.save(scanner_lazy, outFile + 'scanner_lazy.csv')
logicData.save(transmit_lazy, outFile + 'transmit_lazy.csv')

