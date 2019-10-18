import util3 as util
import eta
import os
from pathlib import Path
import time
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc4/")
ETA_FOLDER = DATA_FOLDER / "etaData/"

"""
start with 1x1 seed - have some way of tracking progress
for each g in G get L (don't need to do l max,max)
go through square cases and establish eta
go through non-square cases
do any manual eta if necessary
continue

Files:
etaData = {N : eta(N)}
workingNodes = [n-1,[(g,eta(g)), ]]
"""

MAX_SIZE = 4

def main():
	print("Loading Initial Data")
	#etaData = util.load(DATA_FOLDER / "etaData.dat")
	n_evens = util.load(DATA_FOLDER / "n&evens.dat")
	startN = n_evens[0]
	evens = set(n_evens[1])
	print("Loaded")

	timeBeginExpand = time.time()
	timeStart = timeBeginExpand

	timeDataFile = THIS_FOLDER / "expansionTime.csv"

	with open(timeDataFile, "w") as timeData:

		timeWriter = csv.writer(timeData, dialect='excel')

		timeWriter.writerow(["N", "Time Added", "Total Time"])

		for n in range(startN+1, MAX_SIZE+1):
			timeStart = time.time()

			print("\nExpanding to " + str(n)+"X"+str(n))

			evens = expandLCentric(n, evens)
			timeEnd = time.time()
			timeWriter.writerow([n, timeEnd-timeStart, timeEnd-timeBeginExpand])


def expandLCentric(n, evens):
	prevDir = ETA_FOLDER / (str(n-1)+"X"+str(n-1))
	newDir = ETA_FOLDER / (str(n)+"X"+str(n))
	try:
		os.mkdir(newDir)
	except:
		pass

	#For each l in L
	print("n: " + str(n))
	for i in reversed(range(1, n+1)):
		#reversed(range(1, min(i,n-1)+1)):
		for j in reversed(range(1, min(i,n-1)+1)):
			l = [i,j]
			print("l: " + str(l))

			newEtaData = []

			"""
			if j == 1:
				g = [n-1]*(n-1)
				newEtaData.append(etaLG(l, g, n, evens))
				util.store(newEtaData, newDir / ("f="+str(i)+"_r="+str(j)+".dat") )
				del newEtaData
				continue
			"""

			#f = InvFile, r = InvRank
			for f in range(n-i, n):
				for r in range(n-j, f+1):

					print("f: " + str(f) + "\tr: " + str(r))
					if f == n-1 or r == n-1:
						g = util.genBoard(n-1)
						newEtaData.append(etaLG(l, g, n, evens))
						util.store(newEtaData, newDir / ("f="+str(n-i)+"_r="+str(n-j)+".dat") )
						# continue

					G = util.load(prevDir / ("f="+str(f)+"_r="+str(r)+".dat"))
					G.sort(key = lambda x: unbittenA(x[0]))
					for g in G:
						newEtaData.append(etaLG(l, g[0], n, evens))
						# newWorkingNodes.append(node)
					del G

			util.store(newEtaData, newDir / ("f="+str(n-i)+"_r="+str(n-j)+".dat") )
			del newEtaData
			#storing in case of crash (nothing else is designed to handle a crash)
			# util.store(list(evens), DATA_FOLDER / "evens.dat")
	util.store([[util.genBoard(n),1]], newDir / ("f="+str(n)+"_r="+str(n)+".dat") )

	util.store([n, list(evens)], DATA_FOLDER / "n&evens.dat")
	return evens

def unbittenA(b):
	sum = 0
	print(b)
	for i in range(len(b)):
		sum += (i+2)*b[i][0] + (i+2)*b[i][1]
		if b[i][0] > 0 and b[i][1] > 0:
			sum -= 1
	return sum

def etaLG(l, g, n, evens):
	num = eta.eta(g, l, n, evens)
	node = g + [l]
	print("node: " + str(node))
	if num % 2 == 0:
		evens.add(str(node))
		if len(node) == node[0] and util.file(node) > util.rank(node):
			evens.add(mirror(node))
	return [node, num]

def seed():
	print("Seeding")
	o_o = [[[],0]]

	evens = [str([])]

	try:
		os.mkdir(ETA_FOLDER / "1X1/")
	except:
		pass

	util.store(o_o, ETA_FOLDER / "1X1/f=1_r=1.dat")
	util.store((1,evens), DATA_FOLDER / "n&evens.dat")
	print("Seeded")

def profileIt():
	seed()
	main()

if __name__ == "__main__":
	try:
		os.mkdir(ETA_FOLDER)
	except:
		pass
	seed()
	main()
