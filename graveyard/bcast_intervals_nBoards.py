import logicData
import sys
from operator import itemgetter


# infile_path = "C:/Users/JarlV/Dropbox/Code/2017/capture/bcast_samples/bandwidth_test_2_boards.csv"
inFile = sys.argv[1]
outFile = "output/bcast_intervals_nBoards_output.csv"
outFileTest = "C:/Users/JarlV/Dropbox/Code/2017/capture/bcast_samples/bcast_test_output"
amount_of_mesh_nodes = 2

# logicData.capture(60*12, 2, infile_path, inFile)
data = logicData.LogicData(inFile, "ms", amount_of_mesh_nodes)
data.set_decimal_points(4)
rx_range = (round(0.000222 * data.time_multiplier, data.decimal_points),
            round(0.000226 * data.time_multiplier, data.decimal_points))

# channels = data.get_separated_data_for_channels()

'''''
channels_TxRx_classified = [logicData.classify_toggles_as_Tx_or_Rx(channel, rx_range)
                            for channel in channels]

combined = []
for i in range(len(channels_TxRx_classified)):
    channels_TxRx_classified[i] = [time + [i] for time in channels_TxRx_classified[i]]
    combined += channels_TxRx_classified[i]

final = sorted(combined, key=itemgetter(0))
'''''
# ---------------------------------------------------------------------#
# Another aproach
# ---------------------------------------------------------------------#

def validate_intervals(data, imin, imax):
    imax = imin*(2 ^ imax) # Imax as described in documentation
    interval = imin
    fail_count = 0
    for time in data:
        if interval/2 <= time < interval:
            pass
        elif imin/2 <= time < imin:
            interval = imin
        else:
            print("     test fail on", time, "for interval", interval)
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax
    print("Amount of anomalies in intervals: ", fail_count)
"""
for i in range(len(channels)):
    channels[i] = logicData.calculate_tx_intervals(
        logicData.get_delta_times(channels[i]), rx_range)
    print('Validating node', i)
    validate_intervals(channels[i], 0.020 * data.time_multiplier, 2048)
"""
channels = []
for i in range(amount_of_mesh_nodes):
    logicData.save(channels[i], outFileTest)