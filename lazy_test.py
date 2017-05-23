# Run test:
# lazy_test.py <.csv capture data>
# outputs test result to output folder

import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
outFile = "output/lazy_test_output/"

scanner_lazy = []
transmit_lazy = []

data = logicData.LogicData(inFile, "ms", 8)
data.set_decimal_points(2)
capture_data = data.get_raw_data()

last_sample = 0
for i in capture_data:
    current_transmit_lazy = i[1] & 0b111
    current_transmit_timeout = (i[1] >> 8) ^ (last_sample >> 8)
    current_scanning_lazy = (i[1] >> 3) & 0b111
    current_scanning_timeout = ((i[1] >> 6) & 1) ^ ((last_sample >> 6) & 1)
    if current_scanning_timeout:  # if scanner timeout
        scanner_lazy.append([i[0], current_scanning_lazy])
    if current_transmit_timeout:  # if transmit timeout
        transmit_lazy.append([i[0], current_transmit_lazy])
    last_sample = i[1]

logicData.save(scanner_lazy, outFile + 'scanner_lazy.csv')
logicData.save(transmit_lazy, outFile + 'transmit_lazy.csv')

def slpitlists(list):
    l1=[]
    l2=[]
    for i in list:
        l1.append(i[0])
        l2.append(i[1])
    return [l1, l2]

split_scan = slpitlists(scanner_lazy)
split_trans = slpitlists(transmit_lazy)
print(transmit_lazy)

plt.xlabel("time (ms)")
plt.ylabel("lazy")
plt.plot(split_scan[0], split_scan[1], 'r', label="scan lazy")
plt.plot(split_trans[0], split_trans[1], 'g', label="transmit lazy")
plt.legend()
plt.grid(True)
plt.show()