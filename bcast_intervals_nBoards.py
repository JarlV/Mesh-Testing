import logicData
from operator import itemgetter


infile_path = "C:/Users/JarlVictor/Documents/GitHub/Mesh-Testing/"
inFile = "in_nBoards.csv"
outFile = "out_nBoards.csv"

def test_print(d):
    for i in range(20):
        print(d[i])
    print('')


# logicData.capture(60*12, 2, infile_path, inFile)
data = logicData.LogicData(inFile, "us", 2)
data.set_decimal_points(4)
rx_range = (round(0.000222 * data.time_multiplier, data.decimal_points),
            round(0.000226 * data.time_multiplier, data.decimal_points))

channels = data.get_separated_data_for_channels()
channels_TxRx_classified = [logicData.classify_toggles_as_Tx_or_Rx(channel, rx_range) for channel in channels]

combined = []
for channel in channels_TxRx_classified:
    combined += channel

final = sorted(combined, key=itemgetter(0))

print("should be the same:", len(final), len(data.raw_data))
data.raw_data.pop(0)
for i in range(8):
    print(final[i], data.raw_data[i])

#TODO make test for data in "final"
#test_print(final)
#test_print(data.raw_data)


#logicData.save(calculate_tx_intervals(separated_data[0]), "1"+outFile)
#logicData.save(calculate_tx_intervals(separated_data[1]), "2"+outFile)