import pytest
from disjointset.main import DisjointSet
from edgesets import EdgeSet
from edgesets.generate import GeneratePrimRST, KruskalRSTGenerator
from ggraphs.graph import UndirectedGraph


@pytest.fixture
def ugraph():
    # Kapsalis, 1993 inspired graph (added some edges)
    edges = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 7),
        (2, 3),
        (2, 4),
        (2, 6),
        (2, 5),
        (3, 4),
        (3, 7),
        (3, 6),
        (4, 5),
        (4, 7),
        (6, 7),
        (6, 5),
        (7, 5),
    ]

    graph = UndirectedGraph()

    for u, v in edges:
        graph.add_edge(u, v)

    assert graph.has_edge(7, 3)
    assert graph.has_edge(3, 2)

    return graph


def test_generating_by_prim_rst(ugraph):

    generator = GeneratePrimRST(ugraph)

    tree = generator()

    assert isinstance(tree, EdgeSet)
    assert not tree.is_empty(), "tree shouldn't be empty"

    ds = DisjointSet()
    for v in ugraph.vertices:
        ds.make_set(v)

    for v, u in tree:
        if ds.find(v) == ds.find(u):
            raise RuntimeError("find a cycle")
        ds.union(v, u)

    assert len(ds.get_sets()) == 1, f"len -> {len(ds.get_sets())}"

def test_generating_by_kruskalrst(ugraph):

    generator = KruskalRSTGenerator(ugraph)
    tree = generator()
    assert isinstance(tree, EdgeSet)
    assert not tree.is_empty(), "tree shouldn't be empty"

    ds = DisjointSet()
    for v in ugraph.vertices:
        ds.make_set(v)

    for v, u in tree:
        if ds.find(v) == ds.find(u):
            raise RuntimeError("find a cycle")
        ds.union(v, u)

    assert len(ds.get_sets()) == 1, f"len -> {len(ds.get_sets())}"
