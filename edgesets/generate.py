
import random

from disjointset.main import DisjointSet
from .main import DEdge, EdgeSet, UEdge

class PrimRSTGenerator:

    def __init__(self, graph, directed=False):
        self.graph = graph

        if directed:
            self.EdgeClass = DEdge
        else:
            self.EdgeClass = UEdge


    def __call__(self) -> EdgeSet:
        graph = self.graph
        vertices = set(graph.vertices)

        vi = random.sample(vertices, k=1)[0]
        vertices.remove(vi)

        def done(node):
            return node not in vertices
        def adjacents(node):
            return graph.adjacent_to(node)

        candidates = set()
        for u in adjacents(vi):
            candidates.add(self.EdgeClass(vi, u))

        offspring = EdgeSet()
        while candidates:
            edge = random.sample(candidates, k=1)[0]
            candidates.remove(edge)
            x, y = edge
            if not (done(x) and done(y)):
                offspring.add(edge)
                vf = y if done(x) else x
                for u in adjacents(vf):
                    new_edge = self.EdgeClass(vf, u)
                    if new_edge == edge:
                        continue
                    candidates.add(new_edge)
                # discard by the end
                vertices.discard(x)
                vertices.discard(y)

        return offspring

class KruskalRSTGenerator:

    def __init__(self, graph, directed=False):
        self.graph = graph
        self.edges = [ (v, u) for v, u in graph.edges]

        if directed:
            self.EdgeClass = DEdge
        else:
            self.EdgeClass = UEdge

    def __call__(self):
        offspring = EdgeSet()
        vertices = DisjointSet()

        for v in self.graph.vertices: vertices.make_set(v)

        random.shuffle(self.edges)
        for edge in self.edges:
            v, u = edge
            if vertices.find(v) != vertices.find(u):
                offspring.add(self.EdgeClass(v,u))
                vertices.union(v, u)

        return offspring