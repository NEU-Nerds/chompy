import util3 as util
import eta
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

b = util.genStartBoard(5,7)
# print("file: " + str(util.file(b)))
# print("inverseFile: " + str(util.inverseFile(b)))
# print("rank: " + str(util.rank(b)))
# print("inverseRank: " + str(util.inverseRank(b)))
# print("\nmirrored: " + str(util.mirror(b)))
print("b:" +str(b))
print()
for child in util.getChildren(b):
	print(child)
	print()

# print(util.genStartBoard(3,5))
