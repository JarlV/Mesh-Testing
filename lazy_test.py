# Run test:
# lazy_test.py <.csv capture data>

import logicData
import sys

inFile = sys.argv[1]
outFile = "output/"

scanner_lazy = []
transmit_lazy = []

data = logicData.LogicData(inFile, "s", 8)
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
    last_sample = i[1]

logicData.save(scanner_lazy, outFile + 'scanner_lazy.csv')
logicData.save(transmit_lazy, outFile + 'transmit_lazy.csv')

