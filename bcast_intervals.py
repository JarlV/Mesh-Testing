import logicData

infile_path = "C:/Users/JarlV/Documents/GitHub/"
inFile = "in.csv"
outFile = "out.csv"

def is_in_rx_range(time):
    return time >= rx_range[0] and time <= rx_range[1]

def is_tx_edge(i, j):
    left_is_rx = is_in_rx_range(float(i))
    right_is_rx = is_in_rx_range(float(j))
    #print(float(i), float(j), "edge is tx: ", not right_is_rx and not left_is_rx)
    if left_is_rx & right_is_rx:
        return "Abort" #raise ValueError("Edge is ambiguous", sample_array[index], sample_array[index + 1])
    return not right_is_rx and not left_is_rx

def calculate_tx_intervals(sample_array):
    tx_intervals = []
    current_interval = 0
    for i in range(len(sample_array)-1):
        #print("calculate_tx: ", sample_array[i], sample_array[i+1])
        if is_tx_edge(sample_array[i], sample_array[i+1]) == "Abort":
            # print("At interval", len(tx_intervals)+1, "sample number", i, ". Edge is ambiguous.")
            return tx_intervals
        current_interval += float(sample_array[i])
        if is_tx_edge(sample_array[i], sample_array[i+1]):
            if len(tx_intervals) > 0 and current_interval < tx_intervals[-1]:
                pass # print("At interval", len(tx_intervals)+1, "sample number", i, ". interval is smaller than last interval.")
            tx_intervals.append(current_interval)
            current_interval = 0
    return tx_intervals

def validate_intervals(data, imin, imax):
    for i in data:
        pass

data = logicData.LogicData(inFile, "ms")
data.set_decimal_points(4)
# data.capture(60*5, 1, infile_path)
delta = data.get_delta_times()
rx_range = (0.000222 * data.time_multiplier, 0.000226 * data.time_multiplier)
print(rx_range[0], rx_range[1])
print("samples: ", len(delta))
for i in range(5):
    print(delta[i])
intervals = calculate_tx_intervals(delta)
data.save([[i] for i in intervals], "out.csv")
print("Number of intervals: ", len(intervals))
