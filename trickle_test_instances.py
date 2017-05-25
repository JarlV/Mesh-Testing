import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
amount_of_nodes = int(sys.argv[2])
imin = int(sys.argv[3])
imax = int(sys.argv[4])
outFile = "output/lazy_test_output/"

data = logicData.LogicData(inFile, "ms", amount_of_nodes)
data.set_decimal_points(5)
capture_data = data.get_raw_data()

def get_current_interval(current_bitpattern):
    return [(current_bitpattern >> 3) & 3, (current_bitpattern >> 1) & 3]

def transmits_in_trickle(transmit_times):
    interval = imin
    last_interval = 0
    fail_count = 0
    pass_count = 0
    for t in transmit_times:
        if interval/2 <= t[1] < interval + last_interval/2:
            pass_count += 1
        elif imin/2 <= t[1] < imin + last_interval/2:
            interval = imin
            pass_count += 1
        else:
            fail_count += 1
        if interval * 2 <= imax:
            interval *= 2
        else:
            interval = imax
        last_interval = interval
    return [fail_count, pass_count]

instances_toggle_times = [[[] for i in range(amount_of_nodes+1)] for i in range(amount_of_nodes+1)]
instance_last_toggles = [[0 for i in range(amount_of_nodes+1)] for i in range(amount_of_nodes+1)]
last_sample = [0, 0]

for sample in capture_data:
    if last_sample[1] ^ sample[1] & 1: # If transmit toggles
        ch_i = get_current_interval(sample[1])
        instances_toggle_times[ch_i[0]][ch_i[1]]\
            .append([sample[0], sample[0] - instance_last_toggles[ch_i[0]][ch_i[1]]])
        instance_last_toggles[ch_i[0]][ch_i[1]] = sample[0]
    last_sample = sample

for i in instances_toggle_times:
    for j in i:
        test_result = transmits_in_trickle(j)
        print(test_result[0], "samples failed", test_result[1], "samples passed")


#  Graphics

plt.xlabel("transmit")
plt.ylabel("time (ms) since last transmit")
plt.suptitle("Durations between each transmit")
for row in instances_toggle_times:
    for t_times in row:
        plt.plot([i[0] for i in t_times], [i[1] for i in t_times])
plt.grid(True)
plt.show()