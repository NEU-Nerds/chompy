import util3 as util
import eta
import etaExpansion as etaE
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc4/")

# b = [4,3,2]
# print(util.getChoices([4,3,2]))
# print(util.rank(b))
# print(util.file(b))

# data = util.load(DATA_FOLDER / "etaData/13X13/invF=0_invR=1.dat")
#
# num = len(data)
# for i in range(10):
# 	print(data[i])
# for i in range(10):
# 	print(data[-i])
# x = 9
# for i in range(int(num/x) - 5, int(num/x) + 5):
# 	print(data[i])
# # print(data[0])

# data = util.load(DATA_FOLDER / "etaData/4X4/invF=1_invR=2.dat")
# print(data)

print(etaE.getConcurrentLs((7,1)))
