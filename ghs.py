#!/bin/python3

def find_min_edge_in_list(edges_list):
    result = edges_list[0]
    for node in edges_list:
        if node["value"]<result["value"]:
            result=node


def bloc_init(edges_list):
