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

maxGen = 50

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

def drawPlane(pt, ax):
	xs = np.linspace(pt[0][0]-10, pt[0][0]+10, 50)
	zs = np.linspace(pt[0][2]-10, pt[0][2]+10, 50)
	xx, zz = np.meshgrid(xs, zs)
	yy = pt[0][0] + pt[0][1] - xx
	ax.plot_surface(xx, yy, zz, linewidth=0, alpha=0.4)

def drawBounds(ax):
	global maxGen
	xs = np.linspace(0, maxGen)
	ys = np.linspace(0, maxGen)
	# ax.plot(xs, 0, 0)
	ax.plot(xs, xs, xs)

def appendPt(n, arr):
	arr[0].append(n[0])
	if len(n) > 1:
		arr[1].append(n[1])
	else:
		arr[1].append(0)
	if len(n) > 2:
		arr[2].append(n[2])
	else:
		arr[2].append(0)

def main():
	nodes = seed3xN()
	# nodes = load3xN()

	print("Making Plot...")

	fig = plt.figure()
	# ax = fig.add_subplot(111, projection="3d")
	ax = fig.add_subplot(111)

	nE = [[], [], []]
	nO = [[], [], []]
	nB = [[], [], []]
	nI = [[], [], []]

	pts = [ [[1, 0, 0], 0],
			[[4, 2, 2], 0],
			[[11, 7, 5], 0],
			[[15, 10, 7], 0],
			[[18, 12, 9], 0],
			[[26, 19, 11], 0],
			[[29, 20, 14], 0],
			[[35, 24, 17], 0],
			[[39, 27, 19], 0],
			[[46, 32, 22], 0],
			[[50, 35, 24], 0],
			[[52, 36, 26], 0]]

	ptNumber = 8

	# drawBounds(ax)

	drawPlane(pts[ptNumber], ax)

	d = pts[ptNumber][0][0] + pts[ptNumber][0][1]

	for node in nodes.items():
		n = node[1][0]
		eta = node[1][1]
		#check if the node is even or odd
			#if it is odd, check if it is on a line
				#if it is on a line, plot it
			#if it is even, plot it
		if eta % 2 == 0:
			flag = False
			for pt in pts:
				if not n[2] == pt[0][2]:
					continue
				t = 1
				if n[1]-n[0] == pt[0][1]-pt[0][0]:
					pt[1] += 1
					flag = True

			if not flag and n[2] <= pts[ptNumber][0][2] and n[0] + n[1] < d:
				appendPt(n, nE)
			elif not flag and n[2] < pts[ptNumber][0][2]:
				appendPt(n, nB)
			elif not flag:
				appendPt(n, nI)
		else:
			flag = False
			if len(n) < 2:
				continue
			for pt in pts:
				if not n[2] == pt[0][2]:
					continue
				t = 1
				if n[1]-n[0] == pt[0][1]-pt[0][0]:
					flag = True
			if flag:
				#plot the node
				appendPt(n, nO)

	widthsE = [1] * len(nE[0])
	colorsE = ["#00dd00"] * len(nE[0])
	widthsO = [0.5] * len(nO[0])
	colorsO = ["#0000ff"] * len(nO[0])
	widthsB = [1.5] * len(nB[0])
	colorsB = ["#ff0000"] * len(nB[0])
	widthsI = [0.5] * len(nI[0])
	colorsI = ["#ff00ff"] * len(nI[0])
	ax.scatter(nE[0], nE[1], nE[2], c=colorsE, linewidths=widthsE, marker=".")
	ax.scatter(nO[0], nO[1], nO[2], c=colorsO, linewidths=widthsO, marker=".", alpha=0.4)
	ax.scatter(nB[0], nB[1], nB[2], c=colorsB, linewidths=widthsB, marker=".")
	ax.scatter(nI[0], nI[1], nI[2], c=colorsI, linewidths=widthsI, marker=".", alpha=0.2)

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	l = np.linspace(0, 20, 100)
	for pt in pts:
		print("Num Points: " + str(pt[1]))
		plt.plot(pt[0][0]+l, pt[0][1]+l, pt[0][2])

	print(len(nB[0]))

	plt.show()

if __name__ == "__main__":
	main()
