import multiprocessing as mp
import util3 as util

class etaMultiHandler:
	evalQ = None
	outQ = None
	processes = None
	lock = None

	def __init__(self, threads = 6):
		self.evalQ = mp.JoinableQueue()
		self.outQ = mp.Queue()
		self.lock = mp.Lock()
		self.processes = [mp.Process(target=eval, args=(self.evalQ, self.outQ, self.lock), daemon=True) for i in range(threads)]
		for p in self.processes:
			p.start()

	 #item = [node, bite, evens, outQ]
	def add(self, item):
		self.evalQ.put(item)

	def terminate(self):
		for p in self.processes:
			p.terminate()

def eval(q, outQ, lock):
	while True:
		item = q.get()
		if item is None:
			time.sleep(0.001)
			continue
		# print("Evaling object")
		node = item[0]
		bite = item[1]
		evens = item[2]

		child = util.bite(node, bite)
		if inEvens(child, evens) or inEvens(util.mirror(child), evens):
			# print("found evens")
			outQ.put(1)
			# q.cancel_join_thread()
			lock.acquire()
			while not q.empty():
				q.get()
				q.task_done()
			lock.release()
		q.task_done()

def inEvens(node, evens):
	return (str(node) in evens)
