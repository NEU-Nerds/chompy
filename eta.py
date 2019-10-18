import util3 as util
import heritage3
import ast

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK
def eta(g, l, n, evens):
	#print("\neta for g: "+str(g)+" l: "+str(l))
	#rank(g) < n-1 and file(g) < n-1
	#first part for if square
	#g[0] => util.inverseFile(g)
	#len(g) => util.
	if util.rank(g) == util.file(g) and util.rank(g) < n-1 and util.file(g) < n-1:
		#if g = correct first move for a bite
		if util.inverseRank(g) == 1 and util.inverseFile(g) == 1 and g[0][1] == 1:
			#print("SQUARE bite detected for " + str(g))
			if l == [n-1, n-1]:
				return 0
			elif l == [n, n-1]:
				return 1
			#because including mirrors for now
			elif l == [n-1, n]:
				return 1
			else:
				print("This should not have happend - eta case 1")
		#bite at winning square move then calc remaining moves
		else:
			#if l doesn't extend into first col or top row
			if l[0] < n and l[1] < n:
				return 1
			#turned into a rectangle board
			#if l[1] = n then l[0] = n which isn't in L therefore this is for l[0] = n
			#l[0] = n
			else:
				#getLPrime is adding a col to the right
				#getLPrime shouldn't return a full L
				#l[1] was util.getLPrime(g)
				return etaPrime(g, l, evens)
	else:
		#print("wants to be elsa")
		return etaPrime(g, l, evens)

#for not square, only called by eta
def etaPrime(g, l, evens):
	# print("etaPrime gP: " + str(gP)+"\tlP: " + str(lP))
	if str(g) in evens:
		return 1
	#maybe pass in?
	N = g+[l]

	#print("\netaPrime N: "+str(N))
	return etaGraph(N, evens)

#@profile
def etaGraph(node, evens):
	"""
	get children of node,
	for child:
		if childNum is even:
			return 1
	return 0
	"""

	"""
	bites = util.getChoices(node)
	mirrors = []
	for bite in bites:
		child = util.bite(node, bite)
		if str(child) in evens:
			#print("Even child: " + str(child))
			return 1
		else:
			#print("Odd child: " + str(child))
			mirrors.append(child)
		#elif str(util.mirror(child)) in evens:
			#return 1
	for mirror in mirrors:
		if str(util.mirror(child)) in evens:
			return 1
	return 0
	"""

	children = util.getChildren(node)
	for child in children:
		if str(child) in evens:
			return 1
	return 0
