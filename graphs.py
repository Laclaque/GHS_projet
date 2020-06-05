#!/bin/python3

# The fct that creates a graph obj from a file
# Arguments :
#	- fname : the file name to read from
# Returns :{"size":X,"edges":{node:{node:value,...},...}}
def read_graph_from_file(fname):
	graph = {
		"size" : 0,
		"edges" : {}
	}
	with open(fname, 'r') as f_:
		#first, get the size
		graph["size"] = f_.readline()
		graph["size"] = graph["size"][ :-1]
		#then, every line contains an edge
		for line in f_:
			splitLine = line.split()
			##add the arc node1 to node2
			if splitLine[0] not in graph["edges"]:
				#here we discovered another vertice name so add a new adjacency list (dictionnary)
				graph["edges"][splitLine[0]] = {}
			#add the edge to the graph
			graph["edges"][splitLine[0]][splitLine[1]] = splitLine[2]
			##add the arc node2 to node1
			if splitLine[1] not in graph["edges"]:
				#here we discovered another vertice name so add a new adjacency list (dictionnary)
				graph["edges"][splitLine[1]] = {}
			#add the edge to the graph
			graph["edges"][splitLine[1]][splitLine[0]] = splitLine[2]
	print(graph)
	return graph

