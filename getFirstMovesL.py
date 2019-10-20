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

n = 11

etaData = {}
for i in range (1,n+1):
	nFolder = ETA_FOLDER / (str(i)+"X"+str(i)+"/")
	print("Loading: " + str(i)+"X"+str(i))
	for f in range(i):
		# print("f: " + str(f))
		for r in range(max(f,1), i):
			# print("f: " + str(f)+"\tr: " + str(r))
			# if f == 0 and r == 0:
			# 	continue
			partData = util.load(nFolder / ("invF="+str(f)+"_invR="+str(r)+".dat"))
			# print("partData: " + str(partData))
			for nodeN in partData:
				etaData[str(nodeN[0])] = nodeN[1]
	# print("f: " + str(i)+"\tr: " + str(i))
	partData = util.load(nFolder / ("invF="+str(i)+"_invR="+str(i)+".dat"))
	# print("partData: " + str(partData))
	for nodeN in partData:
		etaData[str(nodeN[0])] = nodeN[1]

	print("Loaded")

# if str([2]) in etaData.keys():
#     print("It's there!")
# else:
#     print("Nope sorry")

firstMoves = {}
mirrors = 0
for i in range(2,n+1):
	for j in range(i,n+1):
		fms = []
		emptyB = [j]*i
		children = heritage3.getChildren(emptyB)
		for child in children:
			if str(child) in etaData.keys():
				cNum = etaData[str(child)]
			else:
				mirrors += 1
				cNum = etaData[str(util.mirror(child))]

			# if i == 5 and j == 6:
			# 	print("child: " + str(child) + "\tnum: " + str(cNum))
			if cNum % 2 == 0:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
util.storeJson(firstMoves, DATA_FOLDER / "firstMovesV3-5_new_4.json")
print("Mirrors: " + str(mirrors))
