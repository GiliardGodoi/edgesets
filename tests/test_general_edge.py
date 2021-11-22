import pytest
import random
from string import ascii_uppercase as letters

from edgesets.main import GEdge, UEdge, DEdge

@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_str_method_for_all_edges_classes(EdgeClass):
    name_class = EdgeClass.__name__

    name_class in {"GEdge", "UEdge", "DEdge"}

    n_edge = 100
    values = [(random.choice(letters),
                random.choice(letters)) for _ in range(n_edge)]

    edges = [EdgeClass(v, u) for v, u in values]

    for value, edge in zip(values, edges):
        assert repr(edge) == str(edge)
        if name_class == "UEdge":
            value = tuple(sorted(value))
        assert repr(edge) == "{}({!r}, {!r}, weight={!r})".format(name_class,*value, 1)


@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_eval_from_repr_when_weights_are_different(EdgeClass):

    name_class = EdgeClass.__name__
    n_edge = 100

    values = [(random.choice(letters),
                random.choice(letters)) for _ in range(n_edge)]
    weights = [random.randint(1, 10_000) for _ in range(n_edge)]

    edges = [EdgeClass(*nodes, weight=w) for nodes, w in zip(values, weights)]

    for value, weight, edge in zip(values, weights, edges):
        if name_class == "UEdge":
            value = tuple(sorted(value))
        assert repr(edge) == str(edge)
        assert repr(edge) == "{}({!r}, {!r}, weight={!r})".format(name_class,*value, weight)

        other = eval(repr(edge))
        assert other == edge


@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_contains_method_for_(EdgeClass):

    n_edge = 100
    values = [(random.choice(letters),
                random.choice(letters)) for _ in range(n_edge)]

    edges = [EdgeClass(v, u) for v, u in values]

    for value, edge in zip(values, edges):
        x, y = value
        assert (x in edge) and (y in edge)

@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_weight_parameter_equal_to_one(EdgeClass):
    n_edge = 100
    values = [(random.choice(letters),
                random.choice(letters)) for _ in range(n_edge)]

    edges = [EdgeClass(v, u) for v, u in values]

    assert all(e.weight == 1 for e in edges)

    random.shuffle(edges)
    assert all(e.w == 1 for e in edges)

    random.shuffle(edges)
    assert all(abs(e) == 1 for e in edges)


@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_random_weight_edges(EdgeClass):
    n_edge = 100
    values = [tuple(random.choices(letters, k=2)) for _ in range(n_edge)]

    weigthes = [random.randint(1, 10_000) for _ in range(n_edge)]

    edges = [EdgeClass(*nodes, weight=w) for nodes, w in zip(values, weigthes)]

    assert all(e.weight == w for e, w in zip(edges, weigthes))
    assert all(e.w == w for e, w in zip(edges, weigthes))
    assert all(abs(e) == w for e, w in zip(edges, weigthes))

@pytest.mark.parametrize(
    'EdgeClass',
    [GEdge, UEdge, DEdge]
)
def test_edges_should_not_contains_numeric_node(EdgeClass):
    n_edge = 100

    values = [tuple(random.choices(letters, k=2)) for _ in range(n_edge)]
    weigthes = [random.randint(1, 10_000) for _ in range(n_edge)]

    edges = [EdgeClass(*nodes, weight=w) for nodes, w in zip(values, weigthes)]

    assert all(w not in e for e, w in zip(edges, weigthes))
