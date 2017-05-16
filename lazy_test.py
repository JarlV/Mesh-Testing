import logicData

infile_path = "C:/Users/JarlV/Dropbox/Code/2017/capture/phoenix/"
inFile = infile_path + "lazy_test.csv"

scanner_lazy = []
transmit_lazy = []

#logicData.capture(60, 8, inFile)
data = logicData.LogicData(inFile, "ms", 8)
data.set_decimal_points(2)
capture_data = data.get_raw_data()

last_timeout = 0
for i in capture_data:
    current_transmit_lazy = i[1] & 0b111
    current_transmit_timeout = (i[1] >> 3) & 1
    current_scanning_lazy = (i[1] >> 4) & 0b111
    current_scanning_timeout = (i[1] >> 7) & 1
    #current_timeout = i[1] & 0b00000011
    current_timeout = (current_transmit_timeout << 1) | current_scanning_timeout
    if current_timeout is not last_timeout:
        if current_scanning_timeout:  # if current_timeout is scanner timeout
            scanner_lazy.append([i[0],current_scanning_lazy])
        elif current_transmit_timeout:  # if current_timeout is transmit timeout
            transmit_lazy.append([i[0], current_transmit_lazy])
    last_timeout = current_timeout

print("scanner lazy:", scanner_lazy)
print("transmit lazy:", transmit_lazy)

logicData.save(scanner_lazy, 'scanner_lazy.csv')
logicData.save(transmit_lazy, 'transmit_lazy.csv')