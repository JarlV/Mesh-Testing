import logicData

infile_path = "C:/Users/JarlV/Dropbox/Code/2017/capture/ticker_samples/"
inFile = infile_path + "trickle_2_chn.csv"
outFile = "output/ticker_trickle_output.csv"

def validate_intervals(data, imin, imax):
    imax = imin*(2^imax)
    interval = imin
    fail_count = 0
    print("Imin: ", imin, "Imax: ", imax)
    for time in data:
        if interval/2 <= time < interval:
            pass
        else:
            print("     test fail.", interval/2, "<=", time, " < ", interval, "not true.")
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax
    print("Amount of anomalies in intervals: ", fail_count)

data = logicData.LogicData(inFile, "ms", 2)
data.set_decimal_points(2)
# logicData.capture(30, 1, inFile)
# delta = data.get_all_delta_times()
rx_range = (0.000222 * data.time_multiplier,
            0.000226 * data.time_multiplier)
channels = data.get_separated_data_for_channels()

delta1 = logicData.get_delta_times(channels[0])
delta2 = logicData.get_delta_times(channels[1])

intervals1 = logicData.calculate_tx_intervals(delta1, rx_range)
intervals2 = logicData.calculate_tx_intervals(delta2, rx_range)

# logicData.save(intervals1, outFile)
validate_intervals(intervals1,
                   (0xFF/10000) * data.time_multiplier,
                   8)
