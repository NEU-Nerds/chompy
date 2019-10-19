import util3 as util
import heritage3
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc3/")

#etaData = util.load(DATA_FOLDER / "etaData.json")


#print(etaData[str([5,3,3,3,3])])

#print(util.file([3]))

n = 8

etaData = {}
for i in range (2,n+1):
	print("Loading: " + str(i)+"X"+str(i)+"etaData.json")
	partData = util.load(DATA_FOLDER / (str(i)+"X"+str(i)+"etaData.json"))
	etaData.update(partData)
	print("Loaded")


firstMoves = {}
for i in range(2,n+1):
	for j in range(i,n+1):
		fms = []
		emptyB = [j]*i
		children = heritage3.getChildren(emptyB)
		for child in children:
			if str(child) in etaData.keys():
				cNum = etaData[str(child)]
			else:
				cNum = etaData[str(util.mirror(child))]
			if cNum % 2 == 0:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
util.store(firstMoves, DATA_FOLDER / "firstMovesV3_new.json")
