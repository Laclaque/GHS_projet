#!bin/python3
import sys
import graphs
from datetime import datetime
import os
import exchanges_queues as eq
import multiprocessing as mp
import ghs
import time
import register

### Arguments checking
if len(sys.argv) != 2:
	print("Syntaxe de la commande : scriptG fichierGraphe")
	exit (1)
graphFile = sys.argv[1]

### Program
g_ = graphs.read_graph_from_file(graphFile)
## Queues creation
queues = {}
for node in g_["edges"]:
	queues[node] =  mp.SimpleQueue() # New queue for each node
queues["father"] = mp.SimpleQueue() # +father

## Creates a unique file name for an instance
now = datetime.now() # Current date and time
d_t = now.strftime("%d%m%y_%H%M%S")
fileName = "RAPPORT_"+graphFile+"__"+d_t

## Creates childs and init them
childs = {}
for node in g_["edges"]:
	# Here we adapt the set before the fork to init each node
	set_ = ghs.bloc_initialization(g_["edges"][node], queues, node, fileName+"_node"+node+".txt")
	n = os.fork()
	if n == 0: # We don't want the childs to fork again
		break
	childs[node] = n
##	

## In the child
if n == 0:
	while set_ != "TERMINE":
		msg = eq.recv_from(set_["queues"][set_["i"]], set_["i"], set_["f_"])
		# Start the roll of the blocks
		if msg["type"] == "connect":
			set_ = ghs.bloc_connect(msg["val1"], msg["sender"], set_)
		elif msg["type"] == "initiate":
			set_ = ghs.bloc_initiate(msg["val1"], msg["val2"], msg["val3"], msg["sender"], set_)
		elif msg["type"] == "test":
			set_ = ghs.bloc_test(msg["val1"], msg["val2"], msg["sender"], set_)
		elif msg["type"] == "accept":
			set_ = ghs.bloc_accept(msg["sender"], set_)
		elif msg["type"] == "reject":
			set_ = ghs.bloc_reject(msg["sender"], set_)
		elif msg["type"] == "report":
			set_ = ghs.bloc_report(msg["val1"], msg["sender"], set_)
		elif msg["type"] == "changeroot":
			set_ = ghs.bloc_changeroot(set_)
		elif msg["type"] == "termine":
			end_set_ = set_
			set_ = "TERMINE"
	#msg = eq.recv_from(set_["queues"][set_["i"]], set_["i"], set_["f_"])
	register.set_state(end_set_, end_set_["f_"])
	print("DONE !")
	time.sleep(3)
##

## In the father
else:
	msg = eq.recv_from(queues["father"], "father", None)
	for node, q_ in queues.items():
		eq.send_to(q_, "father", None, "termine", None, None, None, None)
	print("J'ai fini")
##
exit(0)
