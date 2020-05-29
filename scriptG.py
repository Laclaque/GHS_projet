#!bin/python3
from multiprocessing import queues

##ce sont juste des notes pour l'utilisation d'une queue avec fork
queues = {}
queues[id] = multiprocessing.Queue() #declanche une nouvelle queue

n=os.fork()
if (n == 0): #fils
	print(queues[id].get())
else:
	queues[id].put

#ce fichier là permet de lancer tous les forks
#algo global :
#
#lire le fichier pour remplir un objet graph
#crer un dictionnaire avec les id et les queues en se basant sur la liste des sommets dans l'objet graphe (for x in graph["edges"])
#crer un nom de fichier pour cette instance (name+date par exemple ?)
#créer chaque processus forké (les sites) en leur transmettant leur liste d'adjacence + nom du fichier qui contient les msgs
#
#ds les forks :
#appeler l'init
#puis se mettre en lecture sur sa propre queue
#ensuite un case pour chaque valeur possible (blocs en fct du type)
#tester le set si on sort d'un report pour savoir si fini

##ajouter une queue pour contacter le processus pere
#qd fini, envoyer au pere et le pere kill tous les fils

