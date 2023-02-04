import networkx as nx
import random


def random_walk_rst(G: nx.Graph):
    """
    Random Walk based algorithm to return a Random Spanning Tree
    """
    R = nx.Graph()

    nodes = set(G.nodes)
    done = set()
    v_star = random.choice(list(nodes))
    nodes.remove(v_star)
    done.add(v_star)

    while nodes:
        u = random.choice(list(G[v_star]))
        if u not in done:
            R.add_edge(v_star, u)
            done.add(u)
            nodes.remove(u)
        # walk through the next node
        v_star = u

    return R
