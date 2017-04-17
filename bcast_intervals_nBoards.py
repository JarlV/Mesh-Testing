import logicData
from operator import itemgetter


infile_path = "C:/Users/JarlV/Dropbox/Code/2017/capture/bcast_samples/"
inFile = infile_path + "bandwidth_test_2_boards.csv"
outFile = "output/bcast_intervals_nBoards_output.csv"


# logicData.capture(60*12, 2, infile_path, inFile)
data = logicData.LogicData(inFile, "us", 2)
data.set_decimal_points(4)
rx_range = (round(0.000222 * data.time_multiplier, data.decimal_points),
            round(0.000226 * data.time_multiplier, data.decimal_points))

channels = data.get_separated_data_for_channels()
channels_TxRx_classified = [logicData.classify_toggles_as_Tx_or_Rx(channel, rx_range) for channel in channels]

combined = []
for i in range(len(channels_TxRx_classified)):
    channels_TxRx_classified[i] = [time + [i] for time in channels_TxRx_classified[i]]
    combined += channels_TxRx_classified[i]

final = sorted(combined, key=itemgetter(0))

logicData.save(final, outFile)