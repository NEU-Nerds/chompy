import util3 as util
import heritage3
import ast

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK

#returns 1 or 0 for odd or even respectively
def eta(g, l, n, evens):
	# print("\neta for g: "+str(g)+" l: "+str(l))

	#if g is square and top row and left col are not bitten
	if g[0] == len(g)  and util.rank(g) < n-1 and util.file(g) < n-1:

		#if g = correct first move for a bite
		if g[0] == n-1 and ((len(g) == 1 and l[0] > 0) or (len(g) > 1 and g[1] == 1)):
			# print("SQUARE bite detected for " + str(g))

			#if l is doesn't bites bottom of left col or right of top row (means in a loosing square board position)
			if l == (n-1, n-1):
				return 0
			#if l bites bottom of left col or right of top row (means can mirror by doing the oposite)
			elif l == (n, n-1) or l == (n-1, n):
				return 1

			else:
				print("This should not have happend - eta case 1")
				return 1
		#bite at winning square move then calc remaining moves
		else:
			#if l doesn't extend into first col or top row
			if l[0] < n and l[1] < n:
				#bite at 1,1 and win
				return 1
			#turned into a rectangle board
			#if l[1] = n then l[0] = n which isn't in L therefore this is for l[0] = n
			#l[0] = n
			else:
				#getLPrime is adding a col to the right
				#getLPrime shouldn't return a full L
				#l[1] was util.getLPrime(g)
				return etaPrime(g, l[1]-1, evens)
	else:
		#g not square so adjusting l[1] to match
		return etaPrime(g, l[1]-(n-len(g)), evens)

#for not square, only called by eta
def etaPrime(gP, lP, evens):
	# print("etaPrime gP: " + str(gP)+"\tlP: " + str(lP))
	#if g is even then just play top right
	if inEvens(gP, evens):
		return 1
	#maybe pass in? - the combined node
	N = util.combineGP_LP(gP, lP)
	# print("etaPrime N: "+str(N))

	#relying on graph children logic
	return etaGraph(N, evens)

#@profile
def etaGraph(node, evens):


	bites = util.getChoices(node)
	mirrors = []

	for bite in bites:
		child = util.bite(node, bite)
		# print("child: " + str(child))
		if inEvens(child, evens):
			# print("Even child: " + str(child))
			return 1
		else:
		# 	#print("Odd child: " + str(child))
			mirrors.append(child)
		# elif inEvens(util.mirror(child), evens):
			# return 1
	for mirror in mirrors:
		if inEvens(util.mirror(mirror), evens):
			# print("Even child: " + str(util.mirror(mirror)))
			return 1
	# print("returning even")
	return 0

def inEvens(node, evens):
	return str(node) in evens
	# return (str(node) in evens[n][util.inverseRank(node)][util.inverseFile(node)])
