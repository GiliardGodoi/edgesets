import networkx as nx
import random

from .edge import Edge


def prim_rst(G: nx.Graph):
    """
    Prim Random Spanning Tree
    """
    P = nx.Graph()
    nodes = set(G.nodes)
    done = set()
    candidates = set()

    v_star = random.choice(list(nodes))
    for u in G.adj[v_star]:
        candidates.add(Edge(v_star, u))

    nodes.remove(v_star)
    done.add(v_star)

    n_count = 0
    n_edges = G.number_of_edges()
    while nodes:
        if n_count > n_edges + 2:
            raise RuntimeError(
                f"An unexpected error occurred: {n_count} > {n_edges + 2}"
            )

        edge = random.choice(list(candidates))
        u, v = edge

        if (u in done) and (v in nodes):
            P.add_edge(u, v)
            nodes.remove(v)
            done.add(v)
            for w in G.adj[v]:
                if w != u:
                    candidates.add(Edge(v, w))
        elif (v in done) and (u in nodes):
            P.add_edge(v, u)
            nodes.remove(u)
            done.add(u)
            for w in G.adj[u]:
                if w != v:
                    candidates.add(Edge(u, w))
        else:
            raise RuntimeError("An unexpected error occurred")
        candidates.remove(edge)

    return P
