from operator import attrgetter

from disjointset import DisjointSet
from .main import EdgeSet

class EvaluateEdgeSet:
    '''Evaluate an edgeset '''

    def __init__(self, func_weight=attrgetter('weight')) :
        self.func_weight = func_weight

    def __call__(self, individual : EdgeSet):
        '''
        Parameters:
            chromosome : is a EdgeSet type or a Bag

        Results :
            _cost : Number
                the edgeset cost
            nro_components : int
                graph components identified
        '''
        assert isinstance(individual, EdgeSet), f"unsupported operation for chromosome type {type(individual)}"

        total_cost = 0
        for edge in individual:
            cost = self.func_weight(edge)
            total_cost += cost

        return total_cost
