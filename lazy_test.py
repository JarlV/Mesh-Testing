import logicData

infile_path = "C:/Users/JarlVictor/Dropbox/Code/2017/capture/"
inFile = infile_path + "lazy_test.csv"

scanner_lazy = []
transmit_lazy = []

data = logicData.LogicData(inFile, "ms", 1)
data.set_decimal_points(2)
logicData.capture(60*2, 8, inFile)
capture_data = data.get_raw_data()

for i in capture_data:
    if i[1] >> 6 == 1:
        scanner_lazy.append(i[1] & 0b00111000)
    elif i[1] >> 6 == 2:
        transmit_lazy.append(i[1] & 0b00000111)

print("scanner lazy:", scanner_lazy, "transmit lazy:", transmit_lazy)