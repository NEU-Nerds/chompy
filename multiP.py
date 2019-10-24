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

	#item = [node, bite, evens]
	def add(self, item):
		self.evalQ.put(item)

	def terminate(self):
		for p in self.processes:
			p.terminate()

def eval(q, outQ, lock):
	while True:
		# lock.acquire()
		item = q.get()
		# lock.release()
		# if item is None:
		# 	print("item was none")
		# 	time.sleep(0.001)
		# 	continue
		print("Evaling object")

		node = item[0]
		bite = item[1]
		evens = item[2]

		child = util.bite(node, bite)
		print("got child")
		if inEvens(child, evens):
			print("found evens")
			outQ.put(1)
			print("put 1 to outQ")
			# q.cancel_join_thread()
			lock.acquire()
			print("Got lock")

			while not q.empty():
				try:
					q.get(0.01)
					q.task_done()
				except:
					print("Excepting")
					break
			print("emptyed q")
			lock.release()
			print("released lock")
		print("finishing")
		# if outQ.empty():
		q.task_done()
		print("task doned")
		print("finished")

def inEvens(node, evens):
	return (str(node) in evens)
