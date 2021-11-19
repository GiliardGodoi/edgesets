import random
from collections import defaultdict
from itertools import chain

from .main import EdgeSet, UEdge


class CrossoverPrimRST:

    def __init__(self, respetful=False):
        self.respectful = respetful

    def __call__(self, parent_blue : EdgeSet, parent_red : EdgeSet) -> EdgeSet:
        assert isinstance(parent_blue, EdgeSet), f'parent_a has to be EdgeSet type. Give was {type(parent_blue)}'
        assert isinstance(parent_red, EdgeSet), f'parent_b has to be EdgeSet type. Give was {type(parent_red)}'

        offspring = EdgeSet()

        adjacencies = defaultdict(set)
        vertices = set()
        # itertools chain returns all items from it1, and them from it2
        for edge in chain(parent_red, parent_blue):
            minor, major = edge
            adjacencies[minor].add(edge)
            if issubclass(type(edge), UEdge):
                adjacencies[major].add(edge)
            vertices.add(minor)
            vertices.add(major)

        vi = random.sample(vertices, k=1)[0]
        vertices.remove(vi)
        candidates = adjacencies[vi].copy()

        while candidates:
            edge = random.sample(candidates, k=1)[0]
            minor, major = edge

            if (minor in vertices) or (major in vertices):
                offspring.add(edge)
                vf = major if major in vertices else minor
                adj = adjacencies[vf].difference(set(edge))
                candidates.update(adj)
                vertices.discard(minor)
                vertices.discard(major)

            candidates.remove(edge)



        return offspring
