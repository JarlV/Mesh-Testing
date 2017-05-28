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

# Start Logic capture
logicData.capture(test_time_seconds, amount_of_capture_channels, inFile_path)

# Import capture
capture_data = logicData.LogicData(inFile_path, 'ms', amount_of_capture_channels).get_raw_data()

first_ready_toggle = 0          # 0 until first READY event
rx = 0                          # sum of radio active in Rx mode
tx = 0                          # sum of radio active in Tx mode

last_sample = capture_data[0]   # Used to locate the toggled pin by comparing to 'curent_sample'
last_ready_toggle = [0, 1]      # [(time at last ready toggle), (boolean 'ready toggle not paired with disable toggle']

# 2D array of transmit times for each instance
instances_toggle_times = [[[] for i in range(3)] for i in range(3)]

# 2D array of last transmit for each instance
instance_last_toggles = [[0 for i in range(3)] for i in range(3)]

# In: channel bit pattern from on capture sample.
# Out: Coordinates for the instance at that sample in the form: [row, col]
def get_current_interval(current_bitpattern):
    return [(current_bitpattern >> 4) & 3, (current_bitpattern >> 2) & 3]

# Remove 20 nm bumps from DISABLE pin from capture data
capture_data = logicData.flat_nano_bumps(capture_data, 0.1)

# Loop over all capture samples
for i in range(1, len(capture_data)):
    ready = capture_data[i][1] & 1                                      # READY event
    ready_toggled = (capture_data[i][1] ^ last_sample[1]) & 1           # READY event toggled
    disable_toggled = (capture_data[i][1] ^ last_sample[1]) >> 1        # DISABLE event toggled
    current_instance = get_current_interval(capture_data[i][1])         # instance index at current sample

    if disable_toggled and first_ready_toggle and last_ready_toggle[1]: # If new radio event has happened.
        active_time = capture_data[i][0] - last_ready_toggle[0][0]      # Recent radio active time
        last_ready_toggle[1] = 0                                        # Last READY event toggle
                                                                        #   paired with DISABLE event toggle
        if ready:                                                       # If ready pin is high radio active time is rx
            rx += active_time                                           # radio active time is added to rx sum

        else:                                                           # radio active time is tx
            tx += active_time                                           # radio active time is added to tx sum

            # Add the duration since the last transmit in the same instance
            # to the list of transmit times of given instance. The time since beginning of transmit is also added.
            instances_toggle_times[current_instance[0]][current_instance[1]] \
                .append([capture_data[i][0],
                         capture_data[i][0] - instance_last_toggles[current_instance[0]][current_instance[1]]])

            # Set the last transmit in corresponding instance to be current sample.
            instance_last_toggles[current_instance[0]][current_instance[1]] = capture_data[i][0]

    elif ready_toggled:                                                 # Radio event is beginning
        first_ready_toggle = 1                                          # Only gets changed at first READY toggle
        last_ready_toggle[0] = capture_data[i]
        last_ready_toggle[1] = 1                                        # Makes sure the ready toggle is not included
                                                                        #   more than one time
    last_sample = capture_data[i]                                       # Allows for compare in next iteration


# --------------------------------- Test results output ---------------------------------

# Test each instance
for row in instances_toggle_times:
    for instance in row:
        if len(instance) > 0:
            failed_indexes = logicData.transmits_in_trickle([i[1] for i in instance], imin, imax)
            print(100 * (len(instance) - len(failed_indexes)) / len(instance), "% of samples passed the trickle test.",
                  len(instance), "total samples.")

# Print radio usage percentage to console
tx_p = 100 * tx / (test_time_seconds * 1000)
rx_p = 100 * rx / (test_time_seconds * 1000)
print("Test for radio uptime: Idle: " + str(100 - (tx_p + rx_p))
      + "% (Tx): " + str(tx_p) + "% "
      + "(Rx): " + str(rx_p) + "%")

# Plot data
def plot_data(data):
    plt.xlabel("time (ms) since start of capture")
    plt.ylabel("time (ms) since last transmission")
    plt.suptitle("Trickle transmission instances")
    for row in data:
        for t_times in row:
            plt.plot([i[0] for i in t_times],
                     [i[1] for i in t_times])
    plt.grid(True)
    plt.show()

plot_data(instances_toggle_times)
