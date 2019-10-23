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

maxGen = 20

def seed4xN():
	global maxGen
	etaData = {}
	for i in range (4,maxGen+1):
		print("Loading: " + str(4)+"X"+str(i)+".json")
		partData = util.load(DATA_FOLDER / (str(4) + "X" + str(i) + ".json"))
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
	util.store(nodes, ANALYSIS_FOLDER / "4xN.json")
	return nodes

def load4xN():
	print("Loading 4xN Data...")
	return util.load(ANALYSIS_FOLDER / "4xN.json")

def drawPlane(pt, ax):
	xs = np.linspace(pt[0][0]-10, pt[0][0]+10, 50)
	zs = np.linspace(pt[0][2]-10, pt[0][2]+10, 50)
	xx, zz = np.meshgrid(xs, zs)
	yy = pt[0][0] + pt[0][1] - xx
	ax.plot_surface(xx, yy, zz, linewidth=0, alpha=0.4)

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
	# nodes = seed4xN()
	nodes = load4xN()

	print("Making Plot...")

	nE = [[[], [], []] for i in range(0, maxGen+1)]
	nO = [[[], [], []] for i in range(0, maxGen+1)]
	# nB = [[], [], []]
	# nI = [[], [], []]

	pts = []

	# ptNumber = 10

	# drawBounds(ax)

	# drawPlane(pts[ptNumber], ax)

	# d = pts[ptNumber][0][0] + pts[ptNumber][0][1]

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

			# if not flag and n[2] <= pts[ptNumber][0][2] and n[0] + n[1] < d:
				# appendPt(n, nE)
			# elif not flag and n[2] < pts[ptNumber][0][2]:
				# appendPt(n, nB)
			# elif not flag:
			appendPt(n, nE[n[3]])
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
			# if flag:
				#plot the node
			appendPt(n, nO[n[3]])


	# widthsB = [1.5] * len(nB[0])
	# colorsB = ["#ff0000"] * len(nB[0])
	# widthsI = [0.5] * len(nI[0])
	# colorsI = ["#ff00ff"] * len(nI[0])

	fig = plt.figure()
	# for i in range(0, 6):
		# ax = fig.add_subplot(2, 3, i+1, projection="3d")
	ax = fig.add_subplot(1, 1, 1, projection="3d")
	i = 2
	widthsE = [1] * len(nE[i][0])
	colorsE = ["#00dd00"] * len(nE[i][0])
	widthsO = [0.2] * len(nO[i][0])
	colorsO = ["#0000ff"] * len(nO[i][0])
	ax.scatter(nE[i][0], nE[i][1], nE[i][2], c=colorsE, linewidths=widthsE, marker=".")
	ax.scatter(nO[i][0], nO[i][1], nO[i][2], c=colorsO, linewidths=widthsO, marker=".", alpha=0.2)
	# ax.scatter(nB[0], nB[1], nB[2], c=colorsB, linewidths=widthsB, marker=".")
	# ax.scatter(nI[0], nI[1], nI[2], c=colorsI, linewidths=widthsI, marker=".", alpha=0.2)

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	# l = np.linspace(0, 20, 100)
	# for pt in pts:
		# print("Num Points: " + str(pt[1]))
		# plt.plot(pt[0][0]+l, pt[0][1]+l, pt[0][2])

	# print(len(nB[0]))

	plt.show()

if __name__ == "__main__":
	main()
