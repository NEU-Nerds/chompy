import numpy as np
import json
"""
A mXn board is an array of ints with length m.
The fist value must be exactly n.
Each subsequent value must be less than or equal to the previous.
Each value represents the number of squares in the row.
The poison is at coordinate 0, 0 (in the top left).
The poison is counted in the number of squares in the first row.
"""

#bite the matrix based board at the coordinates (x, y)
#x, y are 0 indexed. X is the row, Y is the col
#returns the bitten board
# @profile
def bite(b, pos):
	if pos[1] == 0:
		return b[:pos[0]]

	board = b[:]

	for row in range(pos[0], len(board)):
		if board[row] > pos[1]:
			board[row] = pos[1];
		else:
			break;

	# board = [r if r > pos[1] else r for r in b]

	return board

def addRow(boardStates, newM):
	newStates = []
	for board in boardStates:
		if len(board) == newM - 1:
			for i in range(1, board[-1] + 1):
				newBoard = board[:]
				newBoard.append(i)
				newStates.append(newBoard)
	boardStates.extend(newStates)

def addCol(boardStates, newN):
	newStates = []
	for board in boardStates:
		newCol = [0] * len(board)#new array of zeros, with length of board
		for i in range(len(board)):
			if board[i] != newN - 1:
				break
			newCol[i] = 1
			newBoard = [board[j] + newCol[j] for j in range(len(board))]
			#TODO: matrix addition of newBoard and newCol
			newStates.append(newBoard)
	boardStates.extend(newStates)

def getM(board):
	return len(board)

def getN(board):
	return board[0]

#returns a 2d array corresponding to the board state
def toArrayNotation(b):
	return [[0 if i < r else 1 for i in range(b[0])] for r in b]

#the number of cols that have a bite taken out of it, if there are no bites, 0
def file(board):
	return board[0] - board[-1]

def inverseFile(board):
	return board[-1]

#the number of empty squares in the last column, if there are no bites, 0
def inverseRank(board):
	n = board[0]
	for i in range(1, len(board)):
		if board[i] < n:
			return i
	return len(board)

def rank(board):
	return len(board) - inverseRank(board)

#generates a unique key to be used in the dict.
# def dKey(board):
	# keyList = []
	# key = ""
	# for row in board:
		# keyList.append("/" + str(int(row)))
		# key += "/" + str(int(row))
	# return ''.join(keyList[1:])
	# return key[1:]
	# return str(board)

def genEndBoard():
	return [1]

def genBoard(m, n):
	return [n] * m

def getL(board, n):
	L = []
	b = board.copy()
	#l is a tuple (m, n)
	#m is across the row
	#n is down the col
	#print("pre L expansion: "+str(b))
	for i in range(len(b), n-1):
		b.append(0)
	#print("post L expansion: " + str(b))

	#min m is file(board) + 1
	#min n is rank(board) + 1
	#max of both is newSize-1

	L = [(i, j) for i in range(max(n-b[-1], file(b)+1), n+1) for j in range(rank(b)+1, min(i, n-1)+1)]
	if file(b) == 0 and rank(b) == 0:
		L.append((0, 0))

	return L

def getLPrime(board):
	return [i for i in range(rank(board), getM(board))]

def combineG_L(g, l):
	#print("Combining g: " + str(g) + " and l: " + str(l))
	node = g.copy()
	n = g[0] + 1

	#print("g pre expansion: " + str(node))
	for i in range(len(node), n-1):
		node.append(0)
	#print("g post expansion: " + str(node))

	newRow = n - l[0]
	node.append(newRow)
	for i in range(len(node)):
		if i+1 <= len(node) - l[1]:
			node[i] = n

	#if node[-1] == 0:
		#node = node[:-1]
	while node[-1] == 0:
		del node[-1]

	return node

#not checking to see if lP is > inverseRank (means it's assuming l is an allowable l)
def combineGP_LP(gP, lP):
	node = gP.copy()
	n = gP[0] + 1

	for i in range(len(node)-lP):
		node[i] += 1
	return node

# @profile
def getChoices(board):
	choices = [(i, j) for i in range(len(board)) for j in range(board[i])]
	choices = choices[1:]
	return choices

def getMxNFileName(m, n):
	return str(m) + "x" + str(n) + ".json"

def load(fileName):
	with open(fileName, "r") as file:
		jData = file.read()
		data = json.loads(jData)
		return data

def store(data, fileName):
	with open(fileName, "w") as file:
		jData = json.dumps(data)
		file.write(jData)
		return 1

def seed():
	#{key:eta}
	#[(node,eta)]
	etaData = {str([1]):0, str([2]):1, str([2,1]):2, str([2,2]):3}#don't seed [1,1] b/c rows > cols
	evens = [str([1]), str([2,1])]
	workingData = [[2], [2,1], [2,2]]
	return etaData, workingData, evens

# @profile
def mirror(board):
	# [ for i in range(len(board))]
	mirrored = [0] * board[0] #initialize the mirrored rectangular board
	for i in range(board[0]):
		for j in range(len(board)):
			if board[j] > i:
				mirrored[i] += 1
	return mirrored

def fromArr(arr):
	b = []
	for r in arr:
		n = 0
		for c in r:
			if c == 1:
				break
			else:
				n += 1
		b.append(n)
	return b

#can you get from b to c with only 1 bite(b is parent)
def isDirectChild(b, c):
	hasDelta = False#has the value of at least one previous row changed
	changedVal = 0#stores the new value of the changed row
	if len(c) > len(b):
		return False
	c = c[:]
	while len(c) < len(b):#at most
		c.append(0)
	for i in range(len(b)):
		delta = int(c[i]) - b[i]
		if delta > 0:
			return False
		if not delta == 0:
			if hasDelta:
				if not c[i] == changedVal:
					return False
			else:
				hasDelta = True
				changedVal = c[i]
	return True

def toBoard(key):
	# return np.array(key).tolist()
	return key.strip('][').split(', ')

"""
TEST STUFF
"""
def main():
	states = [
	[1], [2], [1,1], [2,1], [2,2]
	]

	b = [5, 5, 4, 2]

	a = toArrayNotation(b)

	nA = [[a[i][j] for i in range(len(b))] for j in range(b[0])]#mirror

	print(np.array(a))
	print(np.array(nA))
	print(fromArr(nA))


if __name__ == "__main__":
	main()
