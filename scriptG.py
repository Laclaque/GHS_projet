#!bin/python3
from multiprocessing import Queue

##ce sont juste des notes pour l'utilisation d'une queue avec fork
queues = {}
queues[id] = Queue() #declanche une nouvelle queue

n=os.fork()
if (n == 0): #fils
	print(queues[id].get())
else:
	queues[id].put

#ds les forks :
#puis se mettre en lecture sur sa propre queue
#ensuite un case pour chaque valeur possible (blocs en fct du type)
#tester le set si on sort d'un report pour savoir si fini

##ajouter une queue pour contacter le processus pere
#qd fini, envoyer au pere et le pere kill tous les fils
import sys
import graphs
from datetime import datetime
import os
import exchanges_queues as eq

##Arguments checking
if len(sys.argv) != NBATTENDU:
	echo "Syntaxe de la commande : scriptG fichierGraphe"
	exit (1)
graphFile = argv[1]
##

g_ = graphs.read_graph_from_file(graphFile)
#queues creation
queues={}
for node in g_["edges"]:
	queues[node] =  Queue() #new queue for each node
queues["father"] = Queue() #+father

#create a unique file name for an instance
now = datetime.now() #current date and time
d_t = now.strftime("%d%m%y_%H%M%S")
fileName = "RAPPORT_"+graphFile+"__"+d_t

##creates childs and init them
childs={}
for node in g_["edges"]:
	#here we adapt the set before the fork to init each node
	set_=ghs.bloc_initialization(g_["edges"][node], queues,node,fileName+"_node"+node+".txt")
	n = os.fork()
	if n = 0: #we don't want the childs to fork again
		break
	childs["node"] = n
##	

##in the child
if n == 0:
	while set_ != "TERMINE":
		msg = eq.recv_from(set_["queues"][set_["i"]], set_["i"], set_["f_"])
		if msg == 
			
##

##in the father
else:
	
##
