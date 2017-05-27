# For every 'disable' toggle, the time since last 'ready' toggle is considered
# active time for the radio. If the pin for 'ready' is HIGH at the time of the
# 'disable' toggle, the radio is considered to be in Rx mode since the time of the
# 'ready' pin toggle. Otherwise, the radio is considered to be in Tx mode since the
# time of the 'ready' pin toggle.

# python mesh_radio_test.py capture-seconds imin imax amount-nodes
# Capture bits from MSB to LSB: instanceY1 instanceY0 instanceX1 instanceX0 DISABLE READY

import logicData
import sys, os
import matplotlib.pyplot as plt

test_time_seconds = int(sys.argv[1])
imin = int(sys.argv[2])
imax = int(sys.argv[3])
amount_of_nodes = int(sys.argv[4])
inFile = '/input/mesh_radio_test_capture.csv'
inFile_path = os.getcwd().replace('\\', '/') + inFile
amount_of_capture_channels = 6

# logicData.capture(test_time_seconds, amount_of_capture_channels, inFile_path)
data = logicData.LogicData(inFile_path, 'ms', amount_of_capture_channels)
data.set_decimal_points(4)
capture_data = data.get_raw_data()

first_ready_toggle = 0          # 0 until first READY event
rx = 0                          # sum of radio active in Rx mode
tx = 0                          # sum of radio active in Tx mode

last_sample = capture_data[0]   # Used to locate the toggled pin by comparing to 'curent_sample'
last_ready_toggle = [0, 1]      # [(time at last ready toggle), (boolean ready toggle paired with disable toggle]

# 2D array of transmit times for each instance
instances_toggle_times = [[[] for i in range(amount_of_nodes+1)] for i in range(amount_of_nodes+1)]

# 2D array of last transmit for each instance
instance_last_toggles = [[0 for i in range(amount_of_nodes+1)] for i in range(amount_of_nodes+1)]

# In: channel bit pattern from on capture sample.
# Out: Coordinates for the instance at that sample in the form: [row, col]
def get_current_interval(current_bitpattern):
    return [(current_bitpattern >> 4) & 3, (current_bitpattern >> 2) & 3]


# Remove 20 nm bumps from DISABLE pin from capture data
capture_data = logicData.flat_nano_bumps(capture_data, 0.1)


# Loop over all capture samples
for i in range(1, len(capture_data)):
    ready = capture_data[i][1] & 1
    ready_toggled = (capture_data[i][1] ^ last_sample[1]) & 1
    disable_toggled = (capture_data[i][1] ^ last_sample[1]) >> 1
    current_instance = get_current_interval(capture_data[i][1])
    if disable_toggled and first_ready_toggle and last_ready_toggle[1]:
        active_time = capture_data[i][0] - last_ready_toggle[0][0]
        last_ready_toggle[1] = 0
        if ready:
            rx += active_time
        else:
            tx += active_time
            instances_toggle_times[current_instance[0]][current_instance[1]] \
                .append([capture_data[i][0],
                         capture_data[i][0] - instance_last_toggles[current_instance[0]][current_instance[1]]])
            instance_last_toggles[current_instance[0]][current_instance[1]] = capture_data[i][0]
    elif ready_toggled:
        first_ready_toggle = 1
        last_ready_toggle[0] = capture_data[i]
        last_ready_toggle[1] = 1
    last_sample = capture_data[i]

# Test each instance
for row in instances_toggle_times:
    for instance in row:
        test_result = logicData.transmits_in_trickle(instance, imin, imax)
        print(test_result[0], "samples failed", test_result[1], "samples passed")

# Print radio usage percentage to console
tx_p = 100 * tx / (test_time_seconds * 1000)
rx_p = 100 * rx / (test_time_seconds * 1000)
print("Idle: " + str(100 - (tx_p + rx_p)) + "% Radio usage (Tx): " + str(tx_p) + "% "
      + "(Rx): " + str(rx_p) + "%")

# Plot data
def plot_data(data):
    for row in data:
        for t_times in row:
            plt.plot([i[0] for i in t_times], [i[1] for i in t_times])
    plt.grid(True)
    plt.show()

plot_data(instances_toggle_times)