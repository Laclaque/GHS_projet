#!/bin/python3

#files must be be formated as follows :
###
#nbOfVertices
#node1 node2 weightOnTheEdge
#node1 node3 weightOnTheEdge
#node2 node1 weightOnTheEdge
#node3 node1 weightOnTheEdge
#...
###
#the file must contain every edge two times as it is considered as lists of neighbors
# in our example node1 has 2neigbors whereas node2 and node3 have only 1 neighbor each

#to comment
#not checked yet
def read_graph_from_file(fname):
    graph = {
            "size" : 0,
            "edges" : {}
            }
    with open(fname, 'r') as f_:
        #first, get the size
        graph["size"] = f_.readline()
        #then, every line contains an edge
        for line in f_:
            splitLine = line.split()
            if splitLine[0] not in graph["edges"]:
                #here we discovered another vertice name so add a new adjacency list (dictionnary)
                graph["edges"][splitLine[0]] = {}
            #add the edge to the graph
            graph["edges"][splitLine[0]][splitLine[1]] = splitLine[2]
    return graph
#la tete d'un graphe :
#graph =
#{  "size" : 3,
#    "edges" :    {"A" :{"B" : 3,"C" : 4},
#                          "B" : {"A" : 3},
#                          "C" : {"A" : 4}
#                         }
#}


#to comment
#not checked yet
def get_adjacencyList_from_graph(graph, node):
    return graph["edges"][node]


