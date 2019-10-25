import util3 as util
import eta
import os
from pathlib import Path
import time
import csv
import multiprocessing as mp
# import multiP

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc6/")
ETA_FOLDER = DATA_FOLDER / "etaData/"
THREADS = 6
MAX_DEPTH = 4

P_HANDLER = None

MAX_SIZE = 13

def main():

	print("Loading Initial Data")
	#etaData = util.load(DATA_FOLDER / "etaData.dat")
	n_evens = util.load(DATA_FOLDER / "n&evens.dat")
	startN = n_evens[0]
	#evens is a set of the string representation of all even nodes
	evens = n_evens[1]
	print("Loaded")

	P_HANDLER = etaMultiHandler(THREADS)

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

	"""
	#generating the list L
	#Largest L first so all children are processed before parents
	L = []
	for i in reversed(range(1, n+1)):
	#l[1] >= l[0], l[1] != n
		for j in reversed(range(1, min(i,n-1)+1)):
			L.append((i,j))
	#only for empty board
	L.append((0,0))
	"""
	L = []
	for i in reversed(range(1,n)):
		L.append(getConcurrentLs((n,i)))
	for i in reversed(range(1,n)):
		L.append(getConcurrentLs((i,1)))
	L.append([[0,0]])

	# print("L: " + str(L))

	for lClass in L:
		# print("\n\nlClass: " + str(lClass))
		#add all l's to a Queue
		#.join that Queue
		#read new evens from outQ
		#update evens

		for l in lClass:
			# print("Adding l: " + str(l))
			P_HANDLER.add((l, n , evens, newDir, prevDir))

		#wait untill all l's are evalled
		P_HANDLER.evalQ.join()

		#get a list of all new even lists from outQ
		newEvenSets = P_HANDLER.getOut()
		#add them to evens
		# print("\n\nnewEvenSets: " + str(newEvenSets)+"\n")
		for evenSet in newEvenSets:
			for item in evenSet:
				# print("Adding to evens: " + item)
				evens.add(item)

		# print("newEvens: " + str(evens))





	#storing the list of evens and the finished n size
	util.store([n, evens], DATA_FOLDER / "n&evens.dat")
	#returning evens so it can be passed in again from main
	return evens

class etaMultiHandler:
	evalQ = None
	outQ = None
	processes = None


	def __init__(self, threads = 6):
		self.evalQ = mp.JoinableQueue()
		self.outQ = mp.Queue()

		self.processes = [mp.Process(target=eval, args=(self.evalQ, self.outQ), daemon=True) for i in range(threads)]
		for p in self.processes:
			p.start()

	#item = [node, bite, evens]
	def add(self, item):
		self.evalQ.put(item)

	def getOut(self):
		ret = []
		while not self.outQ.empty():
			ret.append(self.outQ.get())
		return ret

	def terminate(self):
		for p in self.processes:
			p.terminate()

def eval(q, outQ):
	while True:
		#will hold till and item is got
		item = q.get()

		# if item is None:
		# 	print("item was none")
		# 	time.sleep(0.001)
		# 	continue
		l = item[0]
		n = item[1]
		evens = item[2]
		newDir = item[3]
		prevDir = item[4]

		outQ.put(workL(l, n, evens, newDir, prevDir))

		q.task_done()



def workL(l, n, evens, newDir, prevDir):

	#newEtaData is a list of newly processed nodes, kept up til 1 million then written to disk
	newEtaData = []
	#newEvens is a list of the str of new even nodes
	newEvens = []
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
				# print("G: " + str(G))
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
						newEtaData.append(ret[0])
						# newEvens += ret[1]
						for item in ret[1]:
							evens.add(item)
							newEvens.append(item)

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
	ret = etaLG(l, g, n, evens)


	newEtaData.append(ret[0])
	# newEvens += ret[1]
	for item in ret[1]:
		evens.add(item)
		newEvens.append(item)


	#storing whatever is left for this l
	# print("Storing: " + str(newEtaData))
	util.store(newEtaData, thisDir / (str(fileCount)+".dat") )
	del newEtaData

	return newEvens

#gets the eta value of node=l+g and returns [node, eta]
#returns None if the board was invalid for having a negative in it (why is this happeing?)
#also updates evens if the node is even (and adds the mirror too)
def etaLG(l, g, n, evens):
	node = util.combineG_L(g, l)
	if node[-1] < 0:
		return None
	num = eta.eta(g, l, n, evens)

	#if the node is even add it to newEvens
	newEvens = []
	if num % 2 == 0:

		newEvens.append(str(node))
		# if len(node) == node[0] and util.file(node) > util.rank(node):
		# print("Adding mirror " + str(util.mirror(node)))
		newEvens.append(str(util.mirror(node)))
	return ([node, num], newEvens)

def inEvens(node, evens):
	return (str(node) in evens)
	
#returns a list of l's that can be evaled concurrently
#means that one component of l is less and the other is greator
#neither can generate a direct parent or child to what the other can gen
def getConcurrentLs(l):
	L = []
	for i in range(int( (l[0]-l[1])/2 ) +1 ):
		# print(i)
		L.append((l[0]-i, l[1]+i))
	return L

#get list of concurrent ls with l where l[1] <= lim
def getConcurrentLsLimited(l, lim):
	L = []
	for i in range(int( (l[0]-l[1])/2 ) +1 ):
		# print(i)
		if l[1] + i > lim:
			break
		L.append((l[0]-i, l[1]+i))
	return L

#get a list of lists of l's less then l that can be evalled conccurently
def getSubLs(l):
	L = []
	# print("first")
	for i in reversed(range(1, l[1])):
		# print("l: " + str(l))
		# print("i: " + str(i))
		# print("core l: " + str((l[0]-1,i)))
		levelL = getConcurrentLsLimited((l[0]-1,i),l[1]-1)
		# print("levelL: " + str(levelL))
		L.append(levelL)
	# print("\n\nsecond")
	for i in reversed(range(1, l[0]-1)):
		print(str((i,1)))
		levelL = getConcurrentLsLimited((i,1),l[1]-1)
		L.append(levelL)
	L.append([(0,0)])
	return L

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

	evens = set([str([1])])
	# evens = [ [set([]), set([])], [set([]), set([str([1])])] ]
	util.store([[[1],0]], ETA_FOLDER / "1X1/invF=1_invR=1/0.dat")
	util.store([], ETA_FOLDER / "1X1/invF=0_invR=0/0.dat")
	util.store((1,evens), DATA_FOLDER / "n&evens.dat")
	print("Seeded")

def profileIt():
	seed()
	main()

P_HANDLER = etaMultiHandler(THREADS)

if __name__ == "__main__":
	try:
		os.mkdir(ETA_FOLDER)
	except:
		pass
	seed()
	main()
