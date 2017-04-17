import logicData

infile_path = "C:/Users/JarlV/Dropbox/Code/2017/capture/bcast_samples/"
inFile = infile_path + "bandwidth_test_1_board.csv"
outFile = "output/bcast_intervals_output.csv"


def validate_intervals(data, imin, imax):
    imax = imin*(2^imax)
    interval = imin
    fail_count = 0
    for time in data:
        if interval/2 <= time < interval:
            pass
        else:
            print("     test fail on", time, "for interval", interval)
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax
    print("Amount of anomalies in intervals: ", fail_count)

data = logicData.LogicData(inFile, "ms", 1)
data.set_decimal_points(4)
delta = data.get_all_delta_times()
rx_range = (0.000222 * data.time_multiplier,
            0.000226 * data.time_multiplier)
print("samples: ", len(delta))
intervals = logicData.calculate_tx_intervals(delta, rx_range)
logicData.save(intervals, outFile)
print("Number of intervals: ", len(intervals))
validate_intervals(intervals, 0.200*data.time_multiplier, 2024)
