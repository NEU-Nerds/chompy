import utility as util
import numpy as np
import extendBoardStates as ebs
"""
board = util.genBoard(3,5)
board[0][4] = 1
board[0][3] = 1
board[1][4] = 1
board[2][4] = 1
util.display(board)
#board[2][3] = 1
print(util.gamma(board))

data = util.load("./data/3x5TEST3")
print(data)
board = data[0][0]
util.display(board)
print(data[0][1])S
print(data[0][2])
#util.store([(board, [], 1)], "./data/3x5TEST2")



"""

# b1, b2 = util.genBoard(3,5), util.genBoard(3,5)
# util.bite(b1, (0,4))
# util.bite(b1, (2,4))
# util.bite(b2, (1,3))

# print("B1")
# util.display(b1)
# print("B2")
# util.display(b2)

# print(util.delta(b1,b2))
# print(util.isRelated(b1,b2))
# print(util.isDecendent(b2,b1))

"""
extendedBoardStates = util.extendToMxN(3, 3)
# print(len(extendedBoardStates[0][0]))
# print(len(extendedBoardStates[0][0][0]))
for i in range(len(extendedBoardStates[0])):
	print(extendedBoardStates[0][i])
	print("\n")
	children = extendedBoardStates[1][util.dKey(extendedBoardStates[0][i])]
	# print(children)
	for child in children:
		# print(child)
		print("\t" + str(np.array(child)).replace('\n', '\n \t'))
		print("\n")

	# print(extendedBoardStates[1])
	print("\n")
	if i > 50:
		break
"""