#!/bin/python3
import math

def find_min_val_return_key_in_dict(edgesList):
	#verifier si c'est possible de retourner un tuple, sinon garder seulement la
	minimalEdgeKey = min(edgesList, key=edgesList.get)
	return minimalEdgeKey 

def bloc_initialization(edgesList,q_,i):
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
		"edges" : edgesList, #edgesList must contain only neigbors
		"queues" : q_
	}
	for neighbor in edgesList:
		set_["canal"][neighbor] = "basic"
	set_["canal"][find_min_val_return_key_in_dict(edgesList)] = "branch"
	send_to(set_["queues"][minimalEdge],set_["i"],"connect",0, None, None)
	return set_

def bloc_connect(L,j,set_):
	# //!\\vérifier la portée des variables en python
	if L < set_["niv"]:
		set_["canal"][j] = "branch"
		send_to(set["queues"][j],set_["i"],"initiate",set_["niv"],set_["nom"],set_["etat"])
	elif set_["canal"][j] == "basic":
		send_to(set["queues"][set_["i"]],j,"connect",L,None,None) #traiter le message plus tard
	else:
		send_to(set["queues"][j],set_["i"],"initiate",set_["niv"]+1,set_["edges"][j],"find")
		
	return set_

def bloc_initiate(L,F,S,j,set_):
	set_["niv"] = L
	set_["nom"] = F
	set_["etat"] = S
	set_["pere"] = j
	set_["mcan"] = None
	set_["mpoids"] = math.inf
	for vois, val in set_["edges"].item():
		if vois != j &&	if set_["canal"][vois] == "branch":
			send_to(set_["queues"][vois],set_["i"],"initiate",L,F,S)
	if set_["etat"] == "find":
		set_["recu"] = 0
		set = TEST(set_)
	return set_

def TEST(set_):
	exists = {}
	for j, val in set_["canal"].item():
		if j == "basic":
			exists[j] = val
	if not bool(exists) == True:
		j = find_min_val_return_key_in_dict(exists)
		set_["testcan"] = j
		send_to(set["queues"][j],set_["i"],"test",set_["niv"],set_["nom"],None)
	else:
		set_["testcan"] = None
		set_ = REPORT(set_)
	return set_

def bloc_test(L,F,j,set_): 
	if L > set_["niv"]:
		send_to(set_["queues"][set_["i"]],j,"test",L,F,None)
	else:
		if F == set_["nom"]:
			if set_["canal"][j] == "basic":
				set_["canal"][j] = "reject"
			if j != set_["tescan"]:
				send_to(set_["queues"][j],set_["i"],"reject",None,None,None)
			else:
				set_ = TEST(set_)
		else:
			send_to(set_["queues"][j],set_["i"],"accept",None,None,None)
	return set_

def bloc_accept(j,set_):
	set_["tescan"] = None
	if set_["edges"][j] < set_["mpoids"]:
		set_["mpoids"] = set_["edges"][j]
		set_["mcan"] = j
	set_ = REPORT(set_)
	return set_

def bloc_reject(j,set_):
	if set_["canal"][j] == "basic":
		set_["canal"][j] = "reject"
	set_ = TEST(set_)
	return set_

def REPORT(set_):
	test = 0
	for j, val in set_["canal"].item():
		if val == "branch" && j != set["pere"]:
			test = test + 1
	
	if set_["recu"] == test && set_["tescan"] == None:
		set_["etat"] = "found"
		send_to(set_["queues"][set_["pere"]],set["i"], set_["mpoids"],None,None)
	return set_

def bloc_report(poids,j,set_):
	if j != set_["pere"]:
		if set_["poids"] < set_["mpoids"]:
			set_["mpoids"] = set_["poids"]
			set_["mcan"] = j
		set_["recu"] = set_["recu"] + 1
		set_ = REPORT(set_)
	else
		if set_["etat"] == "find":
			send_to(set_["queues"][set_["i"],j,"report",poids,None,None])
		else:
			if set_["poids"] > set_["mpoids"]:
				set_ = CHANGEROOT(set_)
			else:
				if set_["poids"] == set_["mpoids"] && set_["mpoids"] == math.inf:
					return "TERMINE"#//!\\TERMINE
	return set_
