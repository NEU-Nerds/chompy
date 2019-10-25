import multiprocessing as mp
import util3 as util

class etaMultiHandler:
	evalQ = None
	outQ = None
	processes = None


	def __init__(self, threads = 6):
		self.evalQ = mp.JoinableQueue()
		self.outQ = mp.Queue()

		self.processes = [mp.Process(target=eval, args=(self.evalQ, self.outQ), daemon=True) for i in range(threads)]
		for p in self.processes:
			p.start()

	#item = [node, bite, evens]
	def add(self, item):
		self.evalQ.put(item)

	def getOut():
		ret = []
		while not outQ.empty():
			ret.append(outQ.get())
		return ret

	def terminate(self):
		for p in self.processes:
			p.terminate()

def eval(q, outQ):
	while True:
		# lock.acquire()
		item = q.get()
		# lock.release()
		# if item is None:
		# 	print("item was none")
		# 	time.sleep(0.001)
		# 	continue


def inEvens(node, evens):
	return (str(node) in evens)
