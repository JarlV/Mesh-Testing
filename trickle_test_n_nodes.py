import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
amount_of_nodes = int(sys.argv[2])
imin = int(sys.argv[3])
imax = int(sys.argv[3])
outFile = "output/trickle_test_output/"

data = logicData.LogicData(inFile, "ms", amount_of_nodes)
data.set_decimal_points(2)
capture_data = data.get_raw_data()

def changed_node(last_toggle, current_toggle):
    node = last_toggle ^ current_toggle
    counter = 1
    while not node & 1:
        node >>= 1
        counter += 1
    return counter

def transmits_in_trickle(transmit_times):
    interval = imin
    last_interval = 0
    last_t = 0
    for t in transmit_times:
        if interval/2 <= t - last_t < interval + last_interval/2:
            pass
        elif imin/2 <= t - last_t < imin + last_interval/2:
            interval = imin
        else:
            print("FAIL")
        if interval * 2 <= imax:
            interval *= 2
        else:
            interval = imax
        last_interval = interval
        last_t = t

node_toggle_times = [[] for i in range(amount_of_nodes)]
last_capture = [0, 0]
for i in capture_data:
    changed_node = changed_node(last_capture[1], i[1])
    node_toggle_times[changed_node].append(i[0])
    last_capture = i

for i in node_toggle_times:
    transmits_in_trickle(i)

trickle_out_data = 0
logicData.save(trickle_out_data, outFile + 'trickle_n_nodes.csv')

#  Graphics

plt.xlabel("transmit")
plt.ylabel("time (ms) since last transmit")
plt.suptitle("Durations between each transmit")
plt.plot(trickle_out_data)
plt.grid(True)
plt.show()