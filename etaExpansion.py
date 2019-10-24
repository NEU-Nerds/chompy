import util3 as util
import eta
import os
from pathlib import Path
import time
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc6/")
ETA_FOLDER = DATA_FOLDER / "etaData/"



MAX_SIZE = 13

def main():

	print("Loading Initial Data")
	#etaData = util.load(DATA_FOLDER / "etaData.dat")
	n_evens = util.load(DATA_FOLDER / "n&evens.dat")
	startN = n_evens[0]
	#evens is a set of the string representation of all even nodes
	evens = n_evens[1]
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
			#call the main working function
			evens = expandLCentric(n, evens)

			timeEnd = time.time()
			timeWriter.writerow([n, timeEnd-timeStart, timeEnd-timeBeginExpand])
			print("Time elapsed: " + str(timeEnd-timeBeginExpand))
			print("Time for " + str(n)+"X"+str(n) + ": " + str(timeEnd-timeStart))


def expandLCentric(n, evens):
	#expand evens
	for row in evens:
		row.append(set([]))
	evens.append([])
	for i in range(n+1):
		evens[-1].append(set([]))


	#directory of n-1 X n-1 data
	prevDir = ETA_FOLDER / (str(n-1)+"X"+str(n-1))
	#the to be directory of nXn data
	newDir = ETA_FOLDER / (str(n)+"X"+str(n))
	#create the new directory
	try:
		os.mkdir(newDir)
	except:
		#means it's already there
		pass


	#generating the list L
	#Largest L first so all children are processed before parents
	L = []
	for i in reversed(range(1, n+1)):
	#l[1] >= l[0], l[1] != n
		for j in reversed(range(1, min(i,n-1)+1)):
			L.append((i,j))
	#only for empty board
	L.append((0,0))

	for l in L:
		#newEtaData is a list of newly processed nodes, kept up til 1 million then written to disk
		newEtaData = []
		#the number of files written to disk already, incremented each time one is
		fileCount = 0

		#file >= rank
		#MUST DO INVERSE FILE AND RANK BECAUSE SOME BOARDS ARE NOT SQUARE
		#the output directory for this l
		thisDir = newDir / ("invF="+str(n-l[0])+"_invR="+str(n-l[1]))
		try:
			os.mkdir(thisDir)
		except:
			#means it's already there
			pass

		#inverse file of g's to be loaded
		#must be at least inverse file of l (same with rank)
		for f in range(n-l[0],n-1):
			#inverse rank of g's to be loaded
			#inverse rank >= inverse file (but not n-1)
			for r in range(max(n-l[1], f), n-1):

				#the subdir where to find the sepcific r and f g's
				prevSubDir = prevDir / ("invF="+str(f)+"_invR="+str(r))


				#Assuming all files in the dir are our .dat files
				files = os.listdir(prevSubDir)

				for i in range(len(files)):

					#G = list of [node, eta#] pairs
					#g[0] = node fro g in G
					#g[1] = that node's eta
					G = util.load(prevSubDir / (str(i)+".dat"))

					#getting mirrors of each g when neccesary since they aren't stored
					newG = []
					for g in G:
						gF = util.file(g[0])
						gR = util.rank(g[0])

						#check if mirror would have rank and file compatable with l
						if gF < l[1] and gR < l[0] and gF != gR:
							newG.append([util.mirror(g[0]), g[1]])

					G += newG
					#just to remove the referense for garbage collection (don't know if this matters)
					del newG

					#sorting by num choices (least choices first) => earlier nodes don't rely on
					#later nodes as children in etaGraph
					G.sort(key = lambda x: sum(x[0]))

					for g in G:
						#ret = [node, eta#], done this way for profiling
						ret = etaLG(l, g[0], n, evens)
						#if the combined node didn't have any negatives in it (we should fix the root problem of this)
						if ret:
							newEtaData.append(ret)

						del g
						del ret

						#if newEtaData has 1 million nodes in it then write that file and empty newEtaData
						#this is done to limit the memory needed
						if len(newEtaData) >= 1000000:

							#store in a sorted order(don't think this is actually necessary but batching may change)
							newEtaData.sort(key = lambda x: sum(x[0]))
							util.store(newEtaData, thisDir / (str(fileCount)+".dat"))
							#incriment file count
							fileCount += 1
							#making sure garbage collection works - not sure if we need this
							del newEtaData
							newEtaData = []
					del G

		#adding g = empty prev board which is not done in the for loop above
		g = [n-1]*(n-1)
		newEtaData.append(etaLG(l, g, n, evens))

		#storing whatever is left for this l
		util.store(newEtaData, thisDir / (str(fileCount)+".dat") )
		del newEtaData

	#storing the list of evens and the finished n size
	util.store([n, list(evens)], DATA_FOLDER / "n&evens.dat")
	#returning evens so it can be passed in again from main
	return evens

#gets the eta value of node=l+g and returns [node, eta]
#returns None if the board was invalid for having a negative in it (why is this happeing?)
#also updates evens if the node is even (and adds the mirror too)
def etaLG(l, g, n, evens):
	node = util.combineG_L(g, l)
	if node[-1] < 0:
		return None
	num = eta.eta(g, l, n, evens)

	#if the node is even updated evens with node and mirror of node
	if num % 2 == 0:
		evens[util.inverseRank(node)][util.inverseFile(node)].add(str(node))
		#if len(node) == node[0] and util.file(node) > util.rank(node):
		mir = util.mirror(node)
		evens[util.inverseRank(mir)][util.inverseFile(mir)].add(str(mir))
	return [node, num]


def seed():
	print("Seeding")


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

	# evens = [str([1])]
	evens = [ [set([]), set([])], [set([]), set([str([1])])] ]
	util.store([[[1],0]], ETA_FOLDER / "1X1/invF=1_invR=1/0.dat")
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
	# seed()
	main()
