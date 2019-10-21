import util3 as util
import eta
import os
from pathlib import Path
import time
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc5/")
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

MAX_SIZE = 11

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
			print("Time elapsed: " + str(timeEnd-timeBeginExpand))
			print("Time for " + str(n)+"X"+str(n) + ": " + str(timeEnd-timeStart))

"""
batching:
change to folders per inv R and L
store in order of sort
load in order
how store? (1million each?)
stored as number [0,n]
"""
def expandLCentric(n, evens):
	prevDir = ETA_FOLDER / (str(n-1)+"X"+str(n-1))
	newDir = ETA_FOLDER / (str(n)+"X"+str(n))
	try:
		os.mkdir(newDir)
	except:
		pass

	#For each l in L
	# print("\n\nn: " + str(n)+"\n")
	L = []
	#Largest L first
	for i in reversed(range(1, n+1)):
		for j in reversed(range(1, min(i,n-1)+1)):
			L.append((i,j))
	L.append((0,0))

	for l in L:
		newEtaData = []
		fileCount = 0
		# print("\nl: " + str(l))
		#file >= rank
		#MUST DO INVERSE FILE BECAUSE SOME BOARDS NOT SQUARE
		#reg f: range(1,l[0])
		thisDir = newDir / ("invF="+str(n-l[0])+"_invR="+str(n-l[1]))
		try:
			os.mkdir(thisDir)
		except:
			pass
		for f in range(n-l[0],n-1):
			# reg r: range(1,min(f,l[1]-1)+1)
			for r in range(max(n-l[1], f), n-1):
				# print("f: " + str(f)+"\tr: " + str(r))

				prevSubDir = prevDir / ("invF="+str(f)+"_invR="+str(r))


				#Assuming all files are dat files
				files = os.listdir(prevSubDir)
				for i in range(len(files)):

					G = util.load(prevSubDir / (str(i)+".dat"))
					# print("G: " +str(G))
					#getting mirrors

					newG = []
					for g in G:
						# print("g: " + str(g))
						gF = util.file(g[0])
						gR = util.rank(g[0])
						#if mirror would have rank and file compatable
						#also if rank != file?
						if gF < l[1] and gR < l[0] and gF != gR:
							# print("Mirroring")
							# if [util.mirror(g[0]), g[1]] in newG:
							# 	print("Excess mirror " + str(g[0]))
							newG.append([util.mirror(g[0]), g[1]])

					G += newG
					del newG
					# print("postG: " + str(G))
					#sorting by num choices (least choices first) => earlier nodes don't rely on
					#later nodes as children in etaGraph
					G.sort(key = lambda x: sum(x[0]))
					# print("sorted")
					for g in G:
						ret = etaLG(l, g[0], n, evens)
						if ret:
							newEtaData.append(ret)
						del g
						del ret
						if len(newEtaData) > 1000000:
							# print("Storing sub file!")
							#store
							newEtaData.sort(key = lambda x: sum(x[0]))
							util.store(newEtaData, thisDir / (str(fileCount)+".dat"))
							fileCount += 1
							del newEtaData
							newEtaData = []
					del G
		#adding g = empty prev board
		g = [n-1]*(n-1)
		newEtaData.append(etaLG(l, g, n, evens))

		util.store(newEtaData, thisDir / (str(fileCount)+".dat") )
		del newEtaData

	#L = [(0,0)]
	# util.store([[[n]*n,1]], newDir / ("f="+str(n)+"_r="+str(n)+".dat") )

	util.store([n, list(evens)], DATA_FOLDER / "n&evens.dat")
	return evens

def etaLG(l, g, n, evens):
	node = util.combineG_L(g, l)
	if node[-1] < 0:
		return None
	num = eta.eta(g, l, n, evens)

	# print("node: " + str(node) +"\tnum: " + str(num))
	if num % 2 == 0:
		evens.add(str(node))
		#if len(node) == node[0] and util.file(node) > util.rank(node):
		evens.add(str(util.mirror(node)))
	return [node, num]

def seed():
	print("Seeding")
	o_o = [[[1],0]]

	evens = [str([1])]

	try:
		os.mkdir(ETA_FOLDER / "1X1/")
	except:
		pass
	try:
		os.mkdir(ETA_FOLDER / "1X1/invF=1_invR=1/")
	except:
		pass
	try:
		os.mkdir(ETA_FOLDER / "1X1/invF=0_invR=0/")
	except:
		pass

	util.store(o_o, ETA_FOLDER / "1X1/invF=1_invR=1/0.dat")
	util.store([], ETA_FOLDER / "1X1/invF=0_invR=0/0.dat")
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
	#seed()
	main()
