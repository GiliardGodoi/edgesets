
from disjointset import DisjointSet
from .main import EdgeSet

class EvaluateEdgeSet:
    '''Evaluate an edgeset '''

    def __init__(self, base_graph) :
        self.GRAPH = base_graph


    def __call__(self, chromosome, **kwargs):
        '''
        Parameters:
            chromosome : is a EdgeSet type or a Bag

        Results :
            _cost : Number
                the edgeset cost
            nro_components : int
                graph components identified
        '''
        assert isinstance(chromosome, EdgeSet), f"unsupported operation for chromosome type {type(chromosome)}"

        disjointset = DisjointSet()
        _cost = 0
        GRAPH = self.GRAPH

        for v ,u in chromosome:
            if not GRAPH.has_edge(v, u):
                raise RuntimeError("Graph instance has not this edge")
            _cost += GRAPH.weight(v, u)
            if v not in disjointset:
                disjointset.make_set(v)
            if u not in disjointset:
                disjointset.make_set(u)
            disjointset.union(v, u)

        return _cost
