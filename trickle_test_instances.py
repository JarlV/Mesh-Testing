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
    return [current_bitpattern >> 3, current_bitpattern >> 1]

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

instances_toggle_times = [[] for i in range(amount_of_nodes)]
instance_last_toggles = [0 for i in range(amount_of_nodes)]
for sample in capture_data:
    changed_instance = get_current_interval(sample[1])
    instances_toggle_times[changed_instance].append([sample[0], sample[0] - instance_last_toggles[changed_instance]])
    instance_last_toggles[changed_instance] = sample[0]

for i in instances_toggle_times:
    test_result = transmits_in_trickle(i)
    print(test_result[0], "samples failed", test_result[1], "samples passed")


#  Graphics

plt.xlabel("transmit")
plt.ylabel("time (ms) since last transmit")
plt.suptitle("Durations between each transmit")
for i in range(amount_of_nodes):
    plt.plot([j[0] for j in instances_toggle_times[i]], [j[1] for j in instances_toggle_times[i]])
plt.grid(True)
plt.show()