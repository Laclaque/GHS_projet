#!/bin/python3

def find_min_edgeKey_in_adjlist(edgesList):
	#verifier si c'est possible de retourner un tuple, sinon garder seulement la
	minimalEdgeKey = min(edgesList, key=edgesList.get)
	return minimalEdgeKey 

def bloc_init(edgesList,q_,i):
	# //!\\ vérifier la portée des variables en python
	#de toute façon ce bloc n'est appelé qu'une seule fois donc on pourra le mettre dans le code si besoin
	set_ = {
		"i" : i,
		 "canal" : {},
		"niv" : 0,
		"etat" : "found",
		"recu" : 0,
		"nom" : None,
		"pere" : None,
		"mcan" : None,
		"testcan" : None,
		"mpoids" : None,
		"edges" : edgesList,
		"queues" : q_
	}
	for neighbor in edgesList:
		set_["canal"][neighbor] = "basic"
	set_["canal"][find_min_edgeKey_in_adjlist(edgesList)] = "branch"
	send_to(set_["queues"],minimalEdge,"connect",0, None, None)
	return set_

def bloc_connect(L,j,set_):
	# //!\\vérifier la portée des variables en python
	if L < set_["niv"]:
		set_["canal"][j] = "branch"
		send_to(set["queues"],j,"initiate",set_["niv"],set_["nom"],set_["etat"])
	elif set_["canal"][j] = "basic":
		send_to(set["queues"],set["i"],"connect",L,None,None) #traiter le message plus tard
	else:
		send_to(set["queues"],j,"initiate",set_["niv"]+1,set_["edges"][j],"find")
		
	return set_
