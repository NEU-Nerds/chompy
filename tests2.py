import util3 as util
import eta
from pathlib import Path
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

b = [4,3,2]
print(util.getChoices([4,3,2]))
print(util.rank(b))
print(util.file(b))
