from disjointset import DisjointSet
import networkx as nx
import random


def kruskal_rst(G: nx.Graph):
    """
    Kruskal based Random Spanning Tree
    """
    K = nx.Graph()

    disjointset = DisjointSet()
    for v in G.nodes:
        disjointset.make_set(v)

    edges = list(G.edges)

    random.shuffle(edges)
    random.shuffle(edges)  # :()

    for v, u in edges:
        if disjointset.find(v) != disjointset.find(u):
            K.add_edge(v, u)
            disjointset.union(v, u)

    return K
