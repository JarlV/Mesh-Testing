import logicData
import sys, os
import matplotlib.pyplot as plt
# Capture transmission on n boards. 1 channel to 1 pin, toggling on transmission done.
# Run in console: python trickle_test_n_nodes.py [capture-seconds] [Imin] [Imax] [nodes-amount].

test_time_seconds = sys.argv[1]
imin = int(sys.argv[2])
imax = int(sys.argv[3])
amount_of_nodes = int(sys.argv[4])
outFile = "output/"
inFile = '/input/mesh_radio_test_capture.csv'
inFile_path = os.getcwd().replace('\\', '/') + inFile

# Start Logic capture
logicData.capture(test_time_seconds, amount_of_nodes, inFile_path)
data = logicData.LogicData(inFile, "ms", amount_of_nodes)
data.set_decimal_points(5)
capture_data = data.get_raw_data()

def get_changed_node(last_toggle, current_toggle):
    node = last_toggle ^ current_toggle
    counter = 0
    while not node & 1:
        node >>= 1
        counter += 1
    return counter

node_toggle_times = [[] for i in range(amount_of_nodes)]
node_last_toggles = [0 for i in range(amount_of_nodes)]
last_capture = [0, 0]
for sample in capture_data:
    changed_node = get_changed_node(last_capture[1], sample[1])
    node_toggle_times[changed_node].append([sample[0], sample[0] - node_last_toggles[changed_node]])
    node_last_toggles[changed_node] = sample[0]
    last_capture = sample

for i in node_toggle_times:
    failed_indexes = logicData.transmits_in_trickle(i, imin, imax)
    print(100 * (len(i) - len(failed_indexes)) / len(i), "% of samples passed the trickle test.",
          len(i), "total samples.")


#  Graphics

plt.xlabel("transmit")
plt.ylabel("time (ms) since last transmit")
plt.suptitle("Durations between each transmit")
for i in range(amount_of_nodes):
    plt.plot([j[0] for j in node_toggle_times[i]], [j[1] for j in node_toggle_times[i]])
plt.grid(True)
plt.show()