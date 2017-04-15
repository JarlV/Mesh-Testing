import csv
import saleae
import sys
import math


class LogicData:
    time_multiplier = ""
    decimal_points = 2
    new_infile_name = ""
    amount_of_channels = 1
    raw_data = []

    def set_time_multiplier(self, unit):
        if unit == "s":
            self.time_multiplier = 1
        elif unit == "ms":
            self.time_multiplier = 10**3
        elif unit == "us":
            self.time_multiplier = 10**6

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
            formatting = "%." + str(self.decimal_points) + "f"
            delta_times.append(formatting % delta_time)
        return delta_times

    # Get durations between each toggle in the specific data
    def get_delta_times(self, data):
        delta_times = []
        for i in range(0, len(data) - 1):
            delta_time = float(data[i + 1]) - float(data[i])
            formatting = "%." + str(self.decimal_points) + "f"
            delta_times.append(float(formatting % delta_time))
        return delta_times

    # Separates all the data into the channel list it belongs to
    def get_separated_data_for_channels(self):
        separated_data = [[] for i in range(self.amount_of_channels)]
        for i in self.raw_data:
            separated_data[math.ceil((i[1] + 1) / 2) - 1].append(i[0])
        return separated_data

    def get_raw_data(self):
        return self.raw_data

    def set_decimal_points(self, decimal_points):
        self.decimal_points = decimal_points

# Start capture from Logic and export data to file.
# capture_seconds:      amount of time to capture.
# amount_of_channels:   Starting from channel 0, amount of capture channels.
# infile_path:          path to the Logic export file.
def capture(capture_seconds, amount_of_channels, infile_path, inFile):
    s = saleae.Saleae()
    s.set_capture_seconds(capture_seconds)
    s.set_active_channels([i for i in range(amount_of_channels)], [])
    s.set_sample_rate(s.get_all_sample_rates()[0])
    print("capturing... (" + str(capture_seconds) + " seconds)")
    s.capture_start_and_wait_until_finished()
    s.export_data2(infile_path + inFile)

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

# Save data to output file
def save(data, out_file_name):
    if type(data[0]) is not list:
        data = [[i] for i in data]
    if sys.hexversion > 35000000:
        save_py3(data, out_file_name)
    else:
        save_py2(data, out_file_name)

