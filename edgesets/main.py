
import operator
import functools
import reprlib

class GEdge:
    '''General Edge Abrastraction'''
    def __init__(self, u, v, weight=1, **kwargs):
        self._edge = (u, v, weight)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        cls = type(self).__name__
        return "{}({!r}, {!r}, weight={!r})".format(cls,*self._edge)

    def __hash__(self):
        cls = type(self).__name__
        hashes = [hash(cls), hash(self._edge)]
        return functools.reduce(operator.xor, hashes, 0)

    def __contains__(self, vertice):
        return (vertice == self._edge[0]
                or vertice == self._edge[1])

    def __iter__(self):
        yield self._edge[0]
        yield self._edge[1]

    def __getitem__(self, index):
        return self._edge[index]

    def __len__(self):
        return len(self._edge) - 1

    def __abs__(self):
        return self.weight

    def __eq__(self, other):
        return (type(self) == type(other) and
                    self._edge == other._edge )
                    # comparing weight sounds reduntant now
                    # and self.weight == other.weight )

    @property
    def vertices(self):
        for i in [0, 1]:
            yield self._edge[i]

    @property
    def weight(self):
        return self._edge[2]

    @property
    def w(self):
        return self.weight


class UEdge(GEdge):
    '''
    Undirected Edge
    The edges below are suppose to be equal
    Edge<4, 5> == Edge <5, 4>
    '''
    def __init__(self, v, u, **kwargs):
        super().__init__(min(u,v), max(u, v), **kwargs)

class DEdge(GEdge):
    '''Directed Edge'''
    def __init__(self, v, u, **kwargs):
        super().__init__(v, u, **kwargs)


class EdgeSet:

    @classmethod
    def from_iter(cls, items, directed=False):

        def weight(e):
            if len(e) == 3:
                return e[2]
            elif len(e) == 2:
                return 1
            else:
                raise TypeError("items should have 2 arguments for node or at least one for weight")

        Edge = DEdge if directed else UEdge
        result = cls()

        for e in items:
            result.add(Edge(e[0], e[1], weight=weight(e)))

        return result

    def __init__(self):
        self._edges = set()
        self._etype = None

    def __str__(self):
        return repr(self)

    def __repr__(self):
        class_name = type(self).__name__
        if not self._edges:
            return "{}()".format(class_name)
        components = reprlib.repr(self._edges)
        return "{}({})".format(class_name, components)

    def __contains__(self, item):
        return item in self._edges

    def __iter__(self):
        return iter(self._edges)

    def __len__(self):
        return len(self._edges)

    def __bool__(self):
        return bool(self._edges)

    def __sub__(self, other):
        '''- operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for - '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges - other._edges)

    def __and__(self, other):
        '''& operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for & '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges & other._edges)

    def __xor__(self, other):
        '''^ operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for ^ '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges ^ other._edges)

    def __or__(self, other):
        ''' | operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for | '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges | other._edges)

    def __eq__(self, other):
        '''== operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for == '{type(self)}' and {type(other)}")
        return (type(self) == type(other)
                    and len(self) == len(other)
                    and all( e in self for e in other))

    def __lt__(self, other):
        '''< operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for < '{type(self)}' and {type(other)}")
        return self._edges < other._edges

    def __le__(self, other):
        '''<= operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for <= '{type(self)}' and {type(other)}")
        return self._edges <= other._edges

    def __gt__(self, other):
        '''> operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for > '{type(self)}' and {type(other)}")
        return self._edges > other._edges

    def __ge__(self, other):
        '''>= operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for >= '{type(self)}' and {type(other)}")
        return self._edges >= other._edges

    @property
    def vertices(self):
        done = set()
        for edge in self._edges:
            for vertice in edge:
                if vertice not in done:
                    done.add(vertice)
                    yield vertice

    def __check_args(self, param):
        if issubclass(type(param), GEdge):
            return param
        else:
            raise TypeError(f"could not understand input f{param}")

    def add(self, edge):
        edge = self.__check_args(edge)
        if self._etype is None:
            self._etype = type(edge)

        if type(edge) != self._etype:
            raise TypeError('EdgeSet should have the same type of edges')

        self._edges.add(edge)

    def pop(self):
        return self._edges.pop()

    def discard(self, edge):
        if type(edge) == self._etype:
            self._edges.discard(edge)
        else:
            raise TypeError(f"Given edge is not the same type of edges in this EdgeSet. Type: {type(edge)}")

    def remove(self, edge):
        if type(edge) == self._etype:
            self._edges.remove(edge)
        else:
            raise TypeError(f"Given edge is not the same type of edges in this EdgeSet. Type: {type(edge)}")

    def issubset(self, other):
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported method for'{type(self)}' and {type(other)}")
        return self._edges.issubset(other._edges)

    def issuperset(self, other):
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported method for'{type(self)}' and {type(other)}")
        return self._edges.issuperset(other._edges)

    def clear(self):
        self._edges.clear()

    def copy(self):
        result = EdgeSet()
        result._edges = self._edges.copy()
        return result

    def is_empty(self):
        '''Return True if the EdgeSet is empty'''
        return not bool(self)
