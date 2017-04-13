import logicData


infile_path = "C:/Users/JarlVictor/Documents/GitHub/Mesh-Testing/"
inFile = "in_nBoards.csv"
outFile = "out_nBoards.csv"



logicData.capture(60*12, 2, infile_path, inFile)
# data = logicData.LogicData(inFile, "ms")
# data.save(data.get_delta_times(), outFile)