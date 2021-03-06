from random import sample, shuffle

from disjointset import DisjointSet
from ggraphs.steiner.parser import SteinerTreeProblem

from .main import EdgeSet

class RandomWalkRSTBased:

    def __init__(self, stpg):
        self.stpg = stpg

    def __call__(self) -> EdgeSet:
        terminals = set(self.stpg.terminals)
        edges = [(u, v) for u, v in self.stpg.graph.gen_undirect_edges()]
        shuffle(edges)

        done = DisjointSet()
        for v in terminals:
            done.make_set(v)

        individual = EdgeSet()

        while edges and len(done.get_disjoint_sets()) > 1:
            edge = edges.pop()
            y, z = edge[0], edge[1]
            if y not in done: done.make_set(y)
            if z not in done: done.make_set(z)
            if done.find(y) != done.find(z):
                individual.add(y, z)
                done.union(y, z)
                terminals.discard(y)
                terminals.discard(z)

        return individual

class PrimRSTBased:

    def __init__(self, stpg : SteinerTreeProblem):
        self.stpg = stpg

    def __call__(self):

        terminals = set(self.stpg.terminals)
        graph = self.stpg.graph

        vi = sample(range(1, self.stpg.nro_nodes + 1), k=1)[0]

        done   = set()
        edges  = set()
        result = EdgeSet()

        done.add(vi)
        terminals.discard(vi)
        for w in graph.adjacent_to(vi):
            edges.add((vi, w))

        while edges and terminals:
            edge = sample(edges, k=1)[0]
            v, w = edge
            if w not in done:
                done.add(w)
                result.add(v, w)
                terminals.discard(w)
                for u in graph.adjacent_to(w):
                    if u not in done: edges.add((w, u))
            edges.discard((v, w))

        return result

class RandomWalkBased:

    def __init__(self, stpg: SteinerTreeProblem):
        self.stpg = stpg

    def __call__(self):
        graph = self.stpg.graph
        terminals = set(self.stpg.terminals)
        result = EdgeSet()
        done = set()

        v = terminals.pop()
        while terminals:
            done.add(v)
            adjacents = graph.adjacent_to(v, lazy=False)
            u = sample(adjacents, k=1)[0]
            if u not in done:
                result.add(v, u)
            terminals.discard(u)
            v = u
        return result
