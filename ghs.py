#!/bin/python3
import math
import exchanges_queues as eq

# The fct that looks for the minimal value in a dict and returns its key
# Arguments :
#	- edgesList : the dict to search in
# Returns : a key
def find_min_val_return_key_in_dict(edgesList):
	minimalEdgeKey = min(edgesList, key=edgesList.get)
	return minimalEdgeKey 


# The fonction that represents the bloc 1
# Arguments :
#	- edgesList : the adjacency list of the current node to init
#	- q_ : the queues to contact the other nodes
#	- i : the current node to init
#	- f_name : the nam of the file registering the current node activity
# Returns : a set (see above or in PDF)
def bloc_initialization(edgesList,q_,i,f_name):
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
		"queues" : q_,
		"f_" : f_name
	}
	for neighbor in edgesList:
		set_["canal"][neighbor] = "basic"
	minimalEdge = find_min_val_return_key_in_dict(edgesList)
	set_["canal"][minimalEdge] = "branch"
	eq.send_to(set_["queues"][minimalEdge],set_["i"],minimalEdge,"connect",0, None, None, set_["f_"])
	return set_


# The fonction that represents the bloc 2
# Arguments :
#	- L : the arg to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_connect(L,j,set_):
	if L < set_["niv"]:
		set_["canal"][j] = "branch"
		eq.send_to(set_["queues"][j],set_["i"],j,"initiate",set_["niv"],set_["nom"],set_["etat"], set_["f_"])
	elif set_["canal"][j] == "basic":
		eq.send_to(set_["queues"][set_["i"]],j,set_["i"],"connect",L,None,None, set_["f_"]) #traiter le message plus tard
	else:
		eq.send_to(set_["queues"][j],set_["i"],j,"initiate",set_["niv"]+1,set_["edges"][j],"find", set_["f_"])
	return set_


# The fonction that represents the bloc 3
# Arguments :
#	- L, F, S : the args to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_initiate(L,F,S,j,set_):
	set_["niv"] = L
	set_["nom"] = F
	set_["etat"] = S
	set_["pere"] = j
	set_["mcan"] = None
	set_["mpoids"] = math.inf
	for vois, val in set_["edges"].item():
		if vois != j and set_["canal"][vois] == "branch":
			eq.send_to(set_["queues"][vois],set_["i"],vois,"initiate",L,F,S)
	if set_["etat"] == "find":
		set_["recu"] = 0
		set = TEST(set_)
	return set_


# The fonction that represents the bloc 4
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def TEST(set_):
	exists = {}
	for j, val in set_["canal"].item():
		if j == "basic":
			exists[j] = val
	if not bool(exists) == True:
		j = find_min_val_return_key_in_dict(exists)
		set_["testcan"] = j
		eq.send_to(set_["queues"][j],set_["i"],j,"test",set_["niv"],set_["nom"],None)
	else:
		set_["testcan"] = None
		set_ = REPORT(set_)
	return set_


# The fonction that represents the bloc 5
# Arguments :
#	- L, F : the args to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_test(L,F,j,set_): 
	if L > set_["niv"]:
		eq.send_to(set_["queues"][set_["i"]],j,set_["i"],"test",L,F,None)
	else:
		if F == set_["nom"]:
			if set_["canal"][j] == "basic":
				set_["canal"][j] = "reject"
			if j != set_["tescan"]:
				eq.send_to(set_["queues"][j],set_["i"],j,"reject",None,None,None)
			else:
				set_ = TEST(set_)
		else:
			eq.send_to(set_["queues"][j],set_["i"],j,"accept",None,None,None)
	return set_


# The fonction that represents the bloc 6
# Arguments :
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_accept(j,set_):
	set_["tescan"] = None
	if set_["edges"][j] < set_["mpoids"]:
		set_["mpoids"] = set_["edges"][j]
		set_["mcan"] = j
	set_ = REPORT(set_)
	return set_


# The fonction that represents the bloc 7
# Arguments :
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_reject(j,set_):
	if set_["canal"][j] == "basic":
		set_["canal"][j] = "reject"
	set_ = TEST(set_)
	return set_


# The fonction that represents the bloc 8
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def REPORT(set_):
	test = 0
	for j, val in set_["canal"].item():
		if val == "branch" and j != set_["pere"]:
			test = test + 1
	
	if set_["recu"] == test and set_["tescan"] == None:
		set_["etat"] = "found"
		eq.send_to(set_["queues"][set_["pere"]],set_["i"],set_["pere"], set_["mpoids"],None,None)
	return set_


# The fonction that represents the bloc 9
# Arguments :
#	- poids : the arg to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_report(poids,j,set_):
	if j != set_["pere"]:
		if set_["poids"] < set_["mpoids"]:
			set_["mpoids"] = set_["poids"]
			set_["mcan"] = j
		set_["recu"] = set_["recu"] + 1
		set_ = REPORT(set_)
	else:
		if set_["etat"] == "find":
			eq.send_to(set_["queues"][set_["i"],j,set_["i"],"report",poids,None,None])
		else:
			if set_["poids"] > set_["mpoids"]:
				set_ = CHANGEROOT(set_)
			else:
				if set_["poids"] == set_["mpoids"] and set_["mpoids"] == math.inf:
					return "TERMINE"#//!\\TERMINE
	return set_


# The fonction that represents the bloc 10
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def CHANGEROOT(set_):
	if set_["canal"][set_["mcan"]] == "branch":
		eq.send_to(set_["queues"][set_["mcan"]],set_["i"],set_["mcan"],"changeroot",None,None,None)
	else:
		eq.send_to(set_["queues"][set_["mcan"]],set_["i"],set_["mcan"],"connect",set_["niv"],None,None)
		set_["canal"][set_["mcan"]] = branch
	return set_

# The fonction that represents the bloc 11
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see in PDF)
def bloc_changeroot(set_):
	return CHANGEROOT(set_)

