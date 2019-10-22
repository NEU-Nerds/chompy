import util3 as util
import heritage3
import ast
import multiprocessing as mp

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK
def eta(g, l, n, evens, pHandler):
	# print("\neta for g: "+str(g)+" l: "+str(l))
	#rank(g) < n-1 and file(g) < n-1
	#first part for if square
	if g[0] == len(g)  and util.rank(g) < n-1 and util.file(g) < n-1:
		#if g = correct first move for a bite
		# print("roughly square")
		if g[0] == n-1 and ((len(g) == 1 and l[0] > 0) or (len(g) > 1 and g[1] == 1)):
			# print("SQUARE bite detected for " + str(g))
			if l == (n-1, n-1):
				return 0
			elif l == (n, n-1):
				return 1
			#because including mirrors for now
			elif l == (n-1, n):
				return 1
			else:
				# print("This should not have happend - eta case 1")
				return 1
		#bite at winning square move then calc remaining moves
		else:
			#if l doesn't extend into first col or top row
			if l[0] < n and l[1] < n:
				# print("returning here")
				return 1
			#turned into a rectangle board
			#if l[1] = n then l[0] = n which isn't in L therefore this is for l[0] = n
			#l[0] = n
			else:
				#getLPrime is adding a col to the right
				#getLPrime shouldn't return a full L
				#l[1] was util.getLPrime(g)
				return etaPrime(g, l[1]-1, evens, pHandler)
	else:
		#print("wants to be elsa")
		return etaPrime(g, l[1]-(n-len(g)), evens, pHandler)

#for not square, only called by eta
def etaPrime(gP, lP, evens, pHandler):
	# print("etaPrime gP: " + str(gP)+"\tlP: " + str(lP))
	if inEvens(gP, evens):
		return 1
	#maybe pass in?
	N = util.combineGP_LP(gP, lP)
	# print("\netaPrime N: "+str(N))
	return etaGraph(N, evens, pHandler)

#@profile
def etaGraph(node, evens, pHandler):
	#just in case outQ was added to twice
	# print("in etaGraph")
	while not pHandler.outQ.empty():
		# print("emptying outQ")
		pHandler.outQ.get()
	# print("past emptying")
	bites = util.getChoices(node)
	mirrors = []

	#lock so eval process doesn't empty a not yet full Q
	# print("getting lock")
	pHandler.lock.acquire()
	# print("aquired lock")
	# outQ = mp.Queue()
	# print("Adding bites")
	for bite in bites:
		pHandler.add([node, bite, evens])
	pHandler.lock.release()

	#wait till finished
	pHandler.evalQ.join()
	# print("past join")

	if pHandler.outQ.empty():
		# print("outQ was empty")
		return 0
	else:
		ret = pHandler.outQ.get()
		# print("ret: " + str(ret))
		if ret:
			# print("There was an even")
			return 1

	print("This should never have happend what (etaGraph)")
	return 0

def inEvens(node, evens):
	return (str(node) in evens)
