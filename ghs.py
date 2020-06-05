#!/bin/python3
import math
import exchanges_queues as eq
import files_basics as fb
import register
import time

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
# Returns : a set (see above)
def bloc_initialization(edgesList, q_, i, f_name):
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
		"mpoids" : 0.1,
		"edges" : edgesList, #edgesList must contain only neigbors
		"queues" : q_,
		"f_" : f_name
	}
	for neighbor in edgesList:
		set_["canal"][neighbor] = "basic"
	minimalEdge = find_min_val_return_key_in_dict(edgesList)
	set_["canal"][minimalEdge] = "branch"
	fb.write_in_file(set_["f_"], format(set_)+"\n")	
	eq.send_to(set_["queues"][minimalEdge], set_["i"], minimalEdge, "connect", 0, None, None, set_["f_"])
	return set_


# The fonction that represents the bloc 2
# Arguments :
#	- L : the arg to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_connect(L, j, set_):
	if L < set_["niv"]:
		fb.write_in_file(set_["f_"], register.change_var("canal["+j+"]", set_["canal"][j], "branch"))
		set_["canal"][j] = "branch"
		eq.send_to(set_["queues"][j], set_["i"], j, "initiate", set_["niv"], set_["nom"], set_["etat"], set_["f_"])
	else:
		if set_["canal"][j] == "basic":
			time.sleep(1)
			eq.send_to(set_["queues"][set_["i"]], j, set_["i"], "connect", L, None, None, set_["f_"]) #traiter le message plus tard
		else:
			eq.send_to(set_["queues"][j], set_["i"], j, "initiate", set_["niv"]+1, set_["edges"][j], "find", set_["f_"])
	return set_


# The fonction that represents the bloc 3
# Arguments :
#	- L, F, S : the args to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_initiate(L, F, S, j, set_):
	fb.write_in_file(set_["f_"], register.change_var("niv", set_["niv"], L))
	set_["niv"] = L
	fb.write_in_file(set_["f_"], register.change_var("nom", set_["nom"], F))
	set_["nom"] = F
	fb.write_in_file(set_["f_"], register.change_var("etat", set_["etat"], S))
	set_["etat"] = S
	fb.write_in_file(set_["f_"], register.change_var("pere", set_["pere"], j))
	set_["pere"] = j
	fb.write_in_file(set_["f_"], register.change_var("mcan", set_["mcan"], "None"))
	set_["mcan"] = None
	fb.write_in_file(set_["f_"], register.change_var("mpoids", set_["mpoids"], "inf"))
	set_["mpoids"] = math.inf
	for vois, val in set_["edges"].items():
		if vois != j and set_["canal"][vois] == "branch":
			eq.send_to(set_["queues"][vois], set_["i"], vois, "initiate", L, F, S, set_["f_"])
	if set_["etat"] == "find":
		fb.write_in_file(set_["f_"], register.change_var("recu", set_["recu"], 0))
		set_["recu"] = 0
		set_ = TEST(set_)
	return set_


# The fonction that represents the bloc 4
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def TEST(set_):
	exists = {}
	for j, val in set_["canal"].items():
		if val == "basic":
			exists[j] = val
	if not bool(exists) == False: # bool(exists)=False when empty ##POURRAIT ETRE PROBLEMATIQUE
		j = find_min_val_return_key_in_dict(exists)
		fb.write_in_file(set_["f_"], register.change_var("testcan", set_["testcan"], j))
		set_["testcan"] = j
		eq.send_to(set_["queues"][set_["testcan"]], set_["i"], set_["testcan"], "test", set_["niv"], set_["nom"], None, set_["f_"])
	else:
		fb.write_in_file(set_["f_"], register.change_var("testcan", set_["testcan"], "None"))
		set_["testcan"] = None
		set_ = REPORT(set_)
	return set_


# The fonction that represents the bloc 5
# Arguments :
#	- L, F : the args to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_test(L, F, j, set_): 
	if L > set_["niv"]:
		time.sleep(1)
		eq.send_to(set_["queues"][set_["i"]], j, set_["i"], "test", L, F, None, set_["f_"]) # Traiter le msg plus tard
	else:
		if F == set_["nom"]:
			if set_["canal"][j] == "basic":
				fb.write_in_file(set_["f_"], register.change_var("canal["+j+"]", set_["canal"][j], "reject"))
				set_["canal"][j] = "reject"
			if j != set_["testcan"]:
				eq.send_to(set_["queues"][j], set_["i"], j, "reject", None, None, None, set_["f_"])
			else:
				set_ = TEST(set_)
		else:
			eq.send_to(set_["queues"][j], set_["i"], j, "accept", None, None, None, set_["f_"])
	return set_


# The fonction that represents the bloc 6
# Arguments :
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_accept(j, set_):
	fb.write_in_file(set_["f_"], register.change_var("testcan", set_["testcan"], "None"))
	set_["testcan"] = None
	if set_["edges"][j] < set_["mpoids"]:
		fb.write_in_file(set_["f_"], register.change_var("mpoids", set_["mpoids"], set_["edges"][j]))
		set_["mpoids"] = set_["edges"][j]
		fb.write_in_file(set_["f_"], register.change_var("mcan", set_["mcan"], j))
		set_["mcan"] = j
	set_ = REPORT(set_)
	return set_


# The fonction that represents the bloc 7
# Arguments :
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_reject(j, set_):
	if set_["canal"][j] == "basic":
		fb.write_in_file(set_["f_"], register.change_var("canal["+j+"]", set_["canal"][j], "reject"))
		set_["canal"][j] = "reject"
	set_ = TEST(set_)
	return set_


# The fonction that represents the bloc 8
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def REPORT(set_):
	test = 0
	for j, val in set_["canal"].items():
		if val == "branch" and j != set_["pere"]:
			test = test + 1
	if set_["recu"] == test and set_["testcan"] == None:
		fb.write_in_file(set_["f_"], register.change_var("etat", set_["etat"], "found"))
		set_["etat"] = "found"
		eq.send_to(set_["queues"][set_["pere"]], set_["i"], set_["pere"], "report", set_["mpoids"], None, None, set_["f_"])
	return set_


# The fonction that represents the bloc 9
# Arguments :
#	- poids : the arg to run the bloc
#	- j : the sender
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_report(poids, j, set_):
	if j != set_["pere"]:
		if poids < set_["mpoids"]:
			fb.write_in_file(set_["f_"], register.change_var("mpoids", set_["mpoids"], poids))
			set_["mpoids"] = poids
			fb.write_in_file(set_["f_"], register.change_var("mcan", set_["mcan"], j))
			set_["mcan"] = j
		fb.write_in_file(set_["f_"], register.change_var("recu", set_["recu"], set_["recu"]+1))
		set_["recu"] = set_["recu"] + 1
		set_ = REPORT(set_)
	else:
		if set_["etat"] == "find":
			time.sleep(1)
			eq.send_to(set_["queues"][set_["i"]], j, set_["i"], "report", poids, None, None, set_["f_"]) # Traiter le msg plus tard
		else:
			if poids > set_["mpoids"]:
				set_ = CHANGEROOT(set_)
			else:
				if poids == set_["mpoids"] and set_["mpoids"] == math.inf:
					eq.send_finish(set_["queues"]["father"], set_["f_"])
					fb.write_in_file(set_["f_"], " --> "+format(set_)+"\n")
					return "TERMINE" # //!\\ TERMINE
	return set_


# The fonction that represents the bloc 10
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def CHANGEROOT(set_):
	if set_["canal"][set_["mcan"]] == "branch":
		eq.send_to(set_["queues"][set_["mcan"]], set_["i"], set_["mcan"], "changeroot", None, None, None, set_["f_"])
	else:
		eq.send_to(set_["queues"][set_["mcan"]], set_["i"], set_["mcan"], "connect", set_["niv"], None, None, set_["f_"])
		fb.write_in_file(set_["f_"], register.change_var("canal[mcan]", set_["canal"][set_["mcan"]], "branch"))
		set_["canal"][set_["mcan"]] = "branch"
	return set_

# The fonction that represents the bloc 11
# Arguments :
#	- set_ : the set of the current node to update through the bloc
# Returns : a set (see bloc 1)
def bloc_changeroot(set_):
	return CHANGEROOT(set_)

