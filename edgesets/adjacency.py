
from .main import EdgeSet, GEdge

class AdjacencyList:

    def __init__(self, edges : EdgeSet):
        ...

    def __contains__(self, item):
        ...

    def __len__(self):
        ...

    def __bool__(self):
        ...

    @property
    def vertices(self):
        ...

    @property
    def edges(self):
        ...

    def adjacents(self, node) -> GEdge:
        ...