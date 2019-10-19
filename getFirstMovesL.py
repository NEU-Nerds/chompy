import util3 as util
import heritage3
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc4/")
ETA_FOLDER = DATA_FOLDER / "etaData/"
#etaData = util.load(DATA_FOLDER / "etaData.dat")


#print(etaData[str([5,3,3,3,3])])

#print(util.file([3]))

n = 5

etaData = {}
for i in range (1,n+1):
	nFolder = ETA_FOLDER / (str(i)+"X"+str(i)+"/")
	print("Loading: " + str(i)+"X"+str(i))
	for r in range(i):
		for f in range(r+1):
			if f == 0 and r == 0:
				continue
			partData = util.load(nFolder / ("f="+str(f)+"_r="+str(r)+".dat"))
			for nodeN in partData:
				etaData[str(nodeN[0])] = nodeN[1]

	partData = util.load(nFolder / ("f="+str(i)+"_r="+str(i)+".dat"))
	for nodeN in partData:
		etaData[str(nodeN[0])] = nodeN[1]

	print("Loaded")

# if str([[1,1]]) in etaData.keys():
#     print("It's there!")
# else:
#     print("Nope sorry")
print(etaData[str([[0,0],[0,0],[4,2],[5,3]])])
print("\n\n")

firstMoves = {}
mirrors = 0
for i in range(2,n+1):
	for j in range(i,n+1):
		fms = []
		emptyB = util.genStartBoard(i,j)
		print("\ni: " + str(i) + " j: " + str(j))
		print(" start: " + str(emptyB))
		children = util.getChildren(emptyB)
		for child in children:
			# print(str(child) + "\t" + str(etaData[str(child)]))
			if str(child) in etaData.keys():
				cNum = etaData[str(child)]
			else:
				mirrors += 1
				cNum = etaData[str(util.mirror(child))]
			print(str(child) + "\t" + str(cNum))
			if cNum % 2 == 0:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
util.storeJson(firstMoves, DATA_FOLDER / "firstMovesV3-5_new_2.json")
print("Mirrors: " + str(mirrors))
