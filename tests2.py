import util3 as util
import eta
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

b = [[0,0],[2,1]]
print("file: " + str(util.file(b)))
print("inverseFile: " + str(util.inverseFile(b)))
print("rank: " + str(util.rank(b)))
print("inverseRank: " + str(util.inverseRank(b)))
print("\nmirrored: " + str(util.mirror(b)))
print()
for child in util.getChildren(b):
	print(child)
	print()
