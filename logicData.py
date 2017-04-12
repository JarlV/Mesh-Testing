import csv
import saleae
import sys


class LogicData:
    time_multiplier = ""
    decimal_points = 2
    new_infile_name = ""
    raw_data = []

    def save_py3(self, data, out_file_name):
        csv_file = open(out_file_name, 'w', newline='')
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(data)
        csv_file.close()

    def save_py2(self, data, out_file_name):
        with open(out_file_name, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        csvfile.close()
        
    def set_time_multiplier(self, unit):
        if unit == "s":
            self.time_multiplier = 1
        elif unit == "ms":
            self.time_multiplier = 10**3
        elif unit == "us":
            self.time_multiplier = 10**6

    # ----------------------------------------------------------------
    # Interface
    # ----------------------------------------------------------------

    def __init__(self, infile_name, time_multiplier):
        self.new_infile_name = infile_name
        self.set_time_multiplier(time_multiplier)

        # Load data
        csv_file = open(infile_name, 'r')
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        self.raw_data = [float(line[0]) * self.time_multiplier for line in reader]
        csv_file.close()
        print("data loaded")

    # Get durations between each toggle in the data
    def get_delta_times(self):
        delta_times = []
        for i in range(0, len(self.raw_data)-1):
            delta_time = float(self.raw_data[i+1]) - float(self.raw_data[i])
            formatting = "%." + str(self.decimal_points) + "f"
            delta_times.append(formatting % delta_time)
        return delta_times

    # Save data to output file. Data must be 2-dimentional array (row and col)
    def save(self, data, out_file_name):
        if sys.hexversion > 35000000:
            self.save_py3(data, out_file_name)
        else:
            self.save_py2(data, out_file_name)
        print("data saved")

    # Start capture from Logic and export data to file.
    # capture_seconds:      amount of time to capture.
    # amount_of_channels:   Starting from channel 0, amount of capture channels.
    # infile_path:          path to the Logic export file.
    def capture(self, capture_seconds, amount_of_channels, infile_path):
        s = saleae.Saleae()
        s.set_capture_seconds(capture_seconds)
        s.set_active_channels([i for i in range(amount_of_channels)], [])
        s.set_sample_rate(s.get_all_sample_rates()[0])
        s.capture_start_and_wait_until_finished()
        print("capturing... (" + str(capture_seconds) + " seconds)")
        s.export_data2(infile_path + self.new_infile_name)
        print("data exported from Logic")

    def set_decimal_points(self, decimal_points):
        self.decimal_points = decimal_points
