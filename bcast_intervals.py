import logicData

infile_path = "C:/Users/JarlV/Documents/GitHub/"
inFile = "in.csv"
outFile = "out.csv"

def is_in_rx_range(time):
    return time >= rx_range[0] and time <= rx_range[1]

def is_tx_edge(i, j):
    left_is_rx = is_in_rx_range(float(i))
    right_is_rx = is_in_rx_range(float(j))
    if left_is_rx & right_is_rx:
        return "Abort"
    return not right_is_rx and not left_is_rx

def calculate_tx_intervals(sample_array):
    tx_intervals = []
    current_interval = 0
    for i in range(len(sample_array)-1):
        if is_tx_edge(sample_array[i], sample_array[i+1]) == "Abort":
            print("At interval", len(tx_intervals)+1, "sample number", i, ". Edge is ambiguous.")
            return tx_intervals
        current_interval += float(sample_array[i])
        if is_tx_edge(sample_array[i], sample_array[i+1]):
            if len(tx_intervals) > 0 and current_interval < tx_intervals[-1]:
                # The interval did not increase since last interval
                pass # print("At interval", len(tx_intervals)+1, "sample number", i, ". interval is smaller than last interval.")
            tx_intervals.append(current_interval)
            current_interval = 0
    return tx_intervals

def validate_intervals(data, imin, imax):
    print("Validating samples...")
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
    print("Amount of anomalies in samples: ", fail_count)

data = logicData.LogicData(inFile, "us")
data.set_decimal_points(4)

delta = data.get_delta_times()
rx_range = (0.000222 * data.time_multiplier, 0.000226 * data.time_multiplier)
print(rx_range[0], rx_range[1])
print("samples: ", len(delta))
intervals = calculate_tx_intervals(delta)
data.save([[i] for i in intervals], "out.csv")
print("Number of intervals: ", len(intervals))
validate_intervals(intervals, 0.200*data.time_multiplier, 2024)
