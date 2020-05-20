#!bin/python3
from multiprocessing import queues

##ce sont juste des notes pour l'utilisation d'une queue avec fork
queues = {}
queues[id] = multiprocessing.Queue() #declanche une nouvelle queue

n=os.fork()
if (n == 0):
	print(queues[id].get())
else:
	queues[id].put
	
