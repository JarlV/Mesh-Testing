import logicData
#import bcast_intervals


infile_path = "C:/Users/JarlVictor/Documents/GitHub/Mesh-Testing/"
inFile = "in_nBoards.csv"
outFile = "out_nBoards.csv"

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


#TODO make test for n boards
# logicData.capture(60*12, 2, infile_path, inFile)
data = logicData.LogicData(inFile, "us", 2)
rx_range = (0.000222 * data.time_multiplier,
            0.000226 * data.time_multiplier)
separated_data = data.get_separated_data_for_channels()
separated_data = [data.get_delta_times(i) for i in separated_data]


logicData.save(calculate_tx_intervals(separated_data[0]), "1"+outFile)
logicData.save(calculate_tx_intervals(separated_data[1]), "2"+outFile)