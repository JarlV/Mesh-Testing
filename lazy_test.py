import logicData

infile_path = "C:/Users/JarlVictor/Dropbox/Code/2017/capture/"
inFile = infile_path + "lazy_test.csv"

scanner_lazy = []
transmit_lazy = []

data = logicData.LogicData(inFile, "ms", 1)
data.set_decimal_points(2)
#logicData.capture(60*2, 8, inFile)
capture_data = data.get_raw_data()

last_timeout = 0
for i in capture_data:
    current_timeout = i[1] >> 6
    if current_timeout is not last_timeout:
        if current_timeout & 0b01:  # if current_timeout is scanner timeout
            scanner_lazy.append(i[1] & 0b00111000)
        elif current_timeout & 0b10:  # if current_timeout is transmit timeout
            transmit_lazy.append(i[1] & 0b00000111)
    last_timeout = current_timeout

print("scanner lazy:", scanner_lazy, "transmit lazy:", transmit_lazy)