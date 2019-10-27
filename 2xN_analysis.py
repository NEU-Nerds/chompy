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

maxGen = 10

def seed2xN():
	global maxGen
	etaData = {}

	print("Loading: " + str(2)+"X"+str(maxGen)+".json")
	partData = util.load(DATA_FOLDER / (str(2) + "X" + str(maxGen) + ".json"))
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
	util.store(nodes, ANALYSIS_FOLDER / "2xN.json")
	return nodes

def load2xN():
	print("Loading 3xN Data...")
	return util.load(ANALYSIS_FOLDER / "2xN.json")

def drawBounds(ax):
	global maxGen
	xs = np.linspace(0, maxGen)
	ys = np.linspace(0, maxGen)
	# ax.plot(xs, 0, 0)
	ax.plot(xs, xs)

def appendPt(n, arr):
	arr[0].append(n[0])
	if len(n) > 1:
		arr[1].append(n[1])
	else:
		arr[1].append(0)

def drawChildrenLine(n, ax):
	global maxGen
	xs_diag = np.linspace(0, n[1])
	ax.vlines(n[0], 0, n[1])#vertical line
	ax.plot(xs_diag, xs_diag)#diagonal line
	ax.hlines(n[1], n[1], n[0])#horizontal line

def main():
	nodes = seed2xN()
	# nodes = load2xN()

	print("Making Plot...")

	fig = plt.figure()
	ax = fig.add_subplot(111)

	nE = [[], []]
	nO = [[], []]
	nI = [[], []]

	for node in nodes.items():
		n = node[1][0]

		eta = node[1][1]
		#check if the node is even or odd
			#if it is odd, check if it is on a line
				#if it is on a line, plot it
			#if it is even, plot it
		if eta % 2 == 0:
			appendPt(n, nE)
		else:
			if len(n) > 1:
				if n[0] == n[1]:
					appendPt(n, nI)
				else:
					appendPt(n, nO)
			else:
				appendPt(n, nO)

	widthsE = [2] * len(nE[0])
	colorsE = ["#00dd00"] * len(nE[0])
	widthsO = [1] * len(nO[0])
	colorsO = ["#0000ff"] * len(nO[0])
	widthsI = [2] * len(nI[0])
	colorsI = ["#ff00ff"] * len(nI[0])
	ax.scatter(nE[0], nE[1], c=colorsE, linewidths=widthsE, marker="o")
	ax.scatter(nO[0], nO[1], c=colorsO, linewidths=widthsO, marker="o", alpha=0.4)
	ax.scatter(nI[0], nI[1], c=colorsI, linewidths=widthsI, marker="o")

	ax.set_xlabel("X")
	ax.set_ylabel("Y")

	pt = [10, 9]

	drawChildrenLine(pt, ax)

	plt.grid()

	plt.show()

if __name__ == "__main__":
	main()
