import os
import statistics
import tempfile

import pytest
import requests
from disjointset.main import DisjointSet
from edgesets import EdgeSet
from edgesets.evaluation import EvaluateEdgeSet
from edgesets.generate import (KruskalRSTGenerator, PrimRSTGenerator,
                               RandomWalkSTGenerator)
from ggraphs.graph import UndirectedWeightedGraph
from ggraphs.steiner.parser import ParserORLibrary


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

    graph = UndirectedWeightedGraph()

    for u, v in edges:
        graph.add_edge(u, v, weight=1)

    assert graph.has_edge(7, 3)
    assert graph.has_edge(3, 2)

    return graph

@pytest.fixture
def b18graph():
    url = "https://raw.githubusercontent.com/GiliardGodoi/ppgi-stpg-gpx/master/datasets/ORLibrary/steinc18.txt"
    response = requests.get(url)
    content = response.content
    parser = ParserORLibrary()

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as file :
        file.write(content.decode('utf-8'))
        if not os.path.exists(file.name) :
            raise FileNotFoundError('algo estranho aqui')
        stpg = parser.parse(file.name)

    return stpg.graph


def suite_for_one_individual(graph, generator):

    tree = generator()

    assert isinstance(tree, EdgeSet)
    assert not tree.is_empty(), "tree shouldn't be empty"

    ds = DisjointSet()
    for v in graph.vertices:
        ds.make_set(v)

    for v, u in tree:
        if ds.find(v) == ds.find(u):
            raise RuntimeError("find a cycle")
        ds.union(v, u)

    assert len(ds.get_sets()) == 1, f"len -> {len(ds.get_sets())}"

def suite_for_many_individuals(generator):

    evaluator = EvaluateEdgeSet()
    population = [ generator() for _ in range(100)]
    fitness = [ evaluator(p) for p in population]

    assert len(population) == 100
    assert statistics.stdev(fitness) != 0.0


def test_generate_one_individual_with_primrst_and_ugraph(ugraph):
    generator = PrimRSTGenerator(ugraph)
    suite_for_one_individual(ugraph, generator)


def test_generate_one_individual_with_primrst_and_b18_graph(b18graph):
    generator = PrimRSTGenerator(b18graph)
    suite_for_one_individual(b18graph, generator)


def test_generate_many_individuals_with_primrst_and_b18_graph(b18graph):
    generator = PrimRSTGenerator(b18graph)

    suite_for_many_individuals(generator)


def test_generate_one_individual_with_kruskalrst_and_ugraph(ugraph):
    generator = KruskalRSTGenerator(ugraph)
    suite_for_one_individual(ugraph, generator)


def test_generate_one_individual_with_kruskalrst_and_b18_graph(b18graph):
    generator = KruskalRSTGenerator(b18graph)
    suite_for_one_individual(b18graph, generator)


def test_generate_many_individuals_with_kruskalrst_and_b18_graph(b18graph):
    suite_for_many_individuals(KruskalRSTGenerator(b18graph))


def test_generate_one_individual_with_random_walk_and_ugraph(ugraph):
    generator = RandomWalkSTGenerator(ugraph)
    suite_for_one_individual(ugraph, generator)


def test_generate_one_individual_with_random_walk_and_b18_graph(b18graph):
    generator =RandomWalkSTGenerator(b18graph)
    suite_for_one_individual(b18graph, generator)


def test_generate_many_individuals_with_random_walk_and_b18_graph(b18graph):

    suite_for_many_individuals(RandomWalkSTGenerator(b18graph))


