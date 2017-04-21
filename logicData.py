import csv
import saleae
import sys
import math


class LogicData:
    time_multiplier = ""
    formatting = ""
    new_infile_name = ""
    amount_of_channels = 0
    decimal_points = 0
    raw_data = []

    # Set time unit.
    # unit: "s" for seconds, "ms" for milliseconds or "us" for microseconds.
    def set_time_multiplier(self, unit):
        if unit == "s":
            self.time_multiplier = 1
        elif unit == "ms":
            self.time_multiplier = 10**3
        elif unit == "us":
            self.time_multiplier = 10**6

    # Initiate data object
    # infile_name:          Name of csv file exported from Logic analyser
    # time_multiplier:      Time unit for data ("s", "ms", "us")
    # amount_of_channels:   The amount of channels captured from.
    def __init__(self, infile_name, time_multiplier, amount_of_channels):
        self.new_infile_name = infile_name
        self.set_time_multiplier(time_multiplier)
        self.amount_of_channels = amount_of_channels

        # Load data
        csv_file = open(infile_name, 'r')
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        self.raw_data = [[float(line[0]) * self.time_multiplier,
                          int(line[1])] for line in reader]
        csv_file.close()

    # Get durations between each toggle in the data for all the channels
    def get_all_delta_times(self):
        delta_times = []
        for i in range(0, len(self.raw_data)-1):
            delta_time = float(self.raw_data[i+1][0]) - float(self.raw_data[i][0])
            delta_times.append(self.formatting % delta_time)
        return delta_times

    # Separates all the data into the channel list it belongs to
    def get_separated_data_for_channels(self):
        separated_data = [[] for i in range(self.amount_of_channels)]
        for i in self.raw_data:
            separated_data[int(math.ceil(float(i[1] + 1) / 2) - 1)].append(i[0])
        return separated_data

    def get_raw_data(self):
        return self.raw_data

    # Sets decimal points and updates the data
    def set_decimal_points(self, decimal_points):
        self.decimal_points = decimal_points
        self.formatting = "%." + str(decimal_points) + "f"
        self.raw_data = [[round(i[0], self.decimal_points), i[1]] for i in self.raw_data]


# Start capture from Logic and export data to file.
# capture_seconds:      amount of time to capture.
# amount_of_channels:   Starting from channel 0, amount of capture channels.
# infile_path:          path to the Logic export file.
def capture(capture_seconds, amount_of_channels, inFile):
    s = saleae.Saleae()
    s.set_capture_seconds(capture_seconds)
    s.set_active_channels([i for i in range(amount_of_channels)], [])
    s.set_sample_rate(s.get_all_sample_rates()[0])
    print("capturing... (" + str(capture_seconds) + " seconds)")
    s.capture_start_and_wait_until_finished()
    s.export_data2(inFile)

def save_py3(data, out_file_name):
    csv_file = open(out_file_name, 'w', newline='')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerows(data)
    csv_file.close()

def save_py2(data, out_file_name):
    with open(out_file_name, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    csvfile.close()

# Save data to output file path
def save(data, out_file_name):
    if type(data[0]) is not list:
        data = [[i] for i in data]
    if sys.hexversion > 35000000:
        save_py3(data, out_file_name)
    else:
        save_py2(data, out_file_name)

# Returns true if time is in the specified range
def is_in_rx_range(time, rx_range):
    return rx_range[0] <= time <= rx_range[1]

# Returns true if edge is Tx
# i:        first delta time of line-toggle
# j:        second delta time of line-toggle
# rx_range: tuple of highest and lowest number in the group of smallest rx delta times
def is_tx_edge(i, j, rx_range):
    left_is_rx = is_in_rx_range(float(i), rx_range)
    right_is_rx = is_in_rx_range(float(j), rx_range)
    if left_is_rx & right_is_rx:
        return "Abort"
    return not right_is_rx and not left_is_rx

# Returns the delta times of the Tx toggles in the sample array
# sample_array: array of delat times of capture data
# rx_range:     tuple of highest and lowest number in the group of smallest rx delta times
def calculate_tx_intervals(sample_array, rx_range):
    tx_intervals = []
    current_interval = 0
    for i in range(len(sample_array)-1):
        if is_tx_edge(sample_array[i], sample_array[i+1], rx_range) == "Abort":
            print("At interval", len(tx_intervals)+1, "sample number", i, ". Edge is ambiguous.")
            return tx_intervals
        current_interval += float(sample_array[i])
        if is_tx_edge(sample_array[i], sample_array[i+1], rx_range):
            if len(tx_intervals) > 0 and current_interval < tx_intervals[-1]:
                # The interval did not increase since last interval
                pass # print("At interval", len(tx_intervals)+1, "sample number", i, ". interval is smaller than last interval.")
            tx_intervals.append(current_interval)
            current_interval = 0
    return tx_intervals

# Adds a column with value "Tx" or "Rx" for each toggle in d
# d:        single channel capture data
# rx_range: tuple of highest and lowest number in the group of smallest rx delta times
def classify_toggles_as_Tx_or_Rx(d, rx_range):
    data_TxRx = [[d[0]] + ['Xx']]
    delta_times = get_delta_times(d)
    for i in range(len(delta_times) - 1):
        if is_tx_edge(delta_times[i], delta_times[i + 1], rx_range):
            data_TxRx.append([d[i + 1]] + ["Tx"])
        else:
            data_TxRx.append([d[i + 1]] + ["Rx"])
    data_TxRx.append([d[-1]] + ['Xx'])
    return data_TxRx

# Get durations between each toggle in the specified data
def get_delta_times(data):
    delta_times = []
    for i in range(0, len(data) - 1):
        delta_time = float(data[i + 1]) - float(data[i])
        delta_times.append(float(delta_time))
    return delta_times

