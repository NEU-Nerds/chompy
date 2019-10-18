import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
import math
import util3 as util
from mpl_toolkits.mplot3d import Axes3D

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/solved/")
ANALYSIS_FOLDER = Path(THIS_FOLDER, "./data/analysis/")

maxGen = 42

def seed3xN():
	global maxGen
	etaData = {}
	for i in range (3,maxGen+1):
		print("Loading: " + str(3)+"X"+str(i)+".json")
		partData = util.load(DATA_FOLDER / (str(3) + "X" + str(i) + ".json"))
		d = list(partData[1].items())
		for i in range(0, len(d)):
			etaData[d[i][0]] = d[i][1][1]
		print("Loaded")

	print("Converting to New Format...")
	nodes = {}
	for node in etaData.items():
		# print(node[1]) <-- eta
		#get new format from arr
		b = util.revOldDKey(node[0])
		nodes[str(b)] = (b, node[1])
	util.store(nodes, ANALYSIS_FOLDER / "3xN.json")
	return nodes

def load3xN():
	print("Loading 3xN Data...")
	return util.load(ANALYSIS_FOLDER / "3xN.json")

def main():
	# nodes = seed3xN()
	nodes = load3xN()

	print("Making Plot...")

	fig = plt.figure()
	ax = fig.add_subplot(111, projection="3d")

	xE = []
	yE = []
	zE = []
	xO = []
	yO = []
	zO = []

	pts = [ [4, 2, 2],
			[11, 7, 5],
			[15, 10, 7],
			[18, 12, 9],
			[26, 19, 11],
			[29, 20, 14],
			[35, 24, 17],
			[39, 27, 19]]

	for node in nodes.items():
		n = node[1][0]
		eta = node[1][1]
		#check if the node is even or odd
			#if it is odd, check if it is on a line
				#if it is on a line, plot it
			#if it is even, plot it
		if eta % 2 == 0:
			xE.append(n[0])
			if len(n) > 1:
				yE.append(n[1])
			else:
				yE.append(0)
			if len(n) > 2:
				zE.append(n[2])
			else:
				zE.append(0)
		else:
			flag = False
			if len(n) < 2:
				continue
			for pt in pts:
				if not n[2] == pt[2]:
					continue
				t = 1
				# if n[0]/n[1] * pt[1] == pt[0]:
					# flag = True
				if n[1]-n[0] == pt[1]-pt[0]:
					flag = True
				# if not n[1] == pt[1]:
				# 	t = pt[1]/n[1]
				# if n[0] * t == pt[0]:
				# 	flag = True
			if flag:
				#plot the node
				xO.append(n[0])
				if len(n) > 1:
					yO.append(n[1])
				else:
					yO.append(0)
				if len(n) > 2:
					zO.append(n[2])
				else:
					zO.append(0)

	widthsE = [0.1] * len(xE)
	colorsE = ["#00ff00"] * len(xE)
	widthsO = [1] * len(xO)
	colorsO = ["#ff0000"] * len(xO)
	ax.scatter(xE, yE, zE, c=colorsE, linewidths=widthsE, marker=".")
	ax.scatter(xO, yO, zO, c=colorsO, linewidths=widthsO, marker=".")

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	l = np.linspace(0, maxGen, 100)
	for pt in pts:
		plt.plot(pt[0]+l, pt[1]+l, pt[2])

	plt.show()

if __name__ == "__main__":
	main()
