
import pytest
import random
import itertools
from string import ascii_uppercase as letters

from edgesets import EdgeSet, UEdge, DEdge


def get_some_edges(n_edges=100, weighted=False, directed=False):

    Edge = DEdge if directed else UEdge
    values = [(random.choice(letters),
                random.choice(letters)) for _ in range(n_edges)]

    if weighted:
        weights = (random.randint(1, 1000) for _ in range(n_edges))
    else:
        weights = itertools.cycle([1])

    return [Edge(*value, weight=w) for value, w in zip(values, weights)]

def gen_values(w):
        if w:
            return (random.choice(letters),
                    random.choice(letters),
                    random.randint(1, 1000))
        return (random.choice(letters), random.choice(letters), 1)


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_add_to_edgeset_when_all_elements_are_same_type(n_items, directed, weighted):

    values = get_some_edges(n_edges=n_items, directed=directed, weighted=weighted)
    edges = EdgeSet()
    counter = 0
    for e in values:
        if e not in edges:
            counter += 1
        edges.add(e)

    assert len(edges) == counter



@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(10, True, True), (10, True, False),
     (10, False, True), (10, False, False)]
)
def test_add_to_edgeset_when_some_element_has_different_type(n_items, directed, weighted):
    values_1 = get_some_edges(n_edges=n_items, directed=directed, weighted=weighted)

    edges = EdgeSet()
    for e in values_1:
        edges.add(e)

    values_2 = get_some_edges(n_edges=2, directed=(not directed), weighted=weighted)
    with pytest.raises(TypeError):
        for e in values_2:
            edges.add(e)



@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(10, True, True), (10, True, False),
     (10, False, True), (10, False, False)]
)
def test_from_iter_classmethod(n_items, directed, weighted):
    if weighted:
        values = [(random.choice(letters),
                    random.choice(letters), weight) for weight in range(2, n_items + 2)]
    else:
        values = [(random.choice(letters),
                    random.choice(letters)) for _ in range(n_items)]

    edges = EdgeSet.from_iter(values, directed=directed)

    assert len(edges) == n_items

    if directed:
        assert edges._etype == DEdge
    else :
        assert edges._etype == UEdge

    if weighted:
        total_values = sum(v[2] for v in values)
        total_edges = sum(abs(e) for e in edges)
        assert total_values == total_edges
        pass
    else :
        assert all(abs(e) == 1 for e in edges)


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(10, True, True), (10, True, False),
     (10, False, True), (10, False, False)]
)
def test_from_iter_classmethod_with_four_elements_in_some_tuple(n_items, directed, weighted):

    if weighted:
        values = [(random.choice(letters),
                    random.choice(letters),
                    weight ) for weight in range(2, n_items+2)]
    else:
        values = [(random.choice(letters),
                    random.choice(letters)) for _ in range(n_items)]
    values.append(('a', 'z', 4, 'd'))
    random.shuffle(values)

    with pytest.raises(TypeError):
        edges = EdgeSet.from_iter(values, directed=directed)


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(10, True, True), (10, True, False),
     (10, False, True), (10, False, False)]
)
def test_from_iter_classmethod_with_one_element_in_some_tuple(n_items, directed, weighted):

    if weighted:
        values = [(random.choice(letters),
                    random.choice(letters),
                    weight ) for weight in range(2, n_items+2)]
    else:
        values = [(random.choice(letters),
                    random.choice(letters)) for _ in range(n_items)]

    values.append((86))
    random.shuffle(values)

    with pytest.raises(TypeError):
        edges = EdgeSet.from_iter(values, directed=directed)


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_pop_and_bool_method(n_items, directed, weighted):

    def gen_values():
        if weighted:
            return (random.choice(letters),
                    random.choice(letters),
                    random.randint(1, 1000))
        return (random.choice(letters), random.choice(letters), 1)


    values = [ gen_values() for weight in range(n_items)]
    edges = EdgeSet.from_iter(values, directed=directed)

    counter = 0
    while edges:
        _ = edges.pop()
        counter += 1
        if counter > n_items:
            raise RuntimeError(f'count is bigger than n_items: {counter} > {n_items}')


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_clear_method(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    edges = EdgeSet.from_iter(values, directed=directed)

    assert bool(edges)
    assert not edges.is_empty()

    edges.clear()

    assert not bool(edges)
    assert edges.is_empty()

@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_equal_when_edgesets_are_equal(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    e1 = EdgeSet.from_iter(values, directed=directed)

    random.shuffle(values)
    e2 = EdgeSet.from_iter(values, directed=directed)

    assert e1 is not e2
    assert e1 == e2

@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_equal_when_edgesets_has_edges_types_differents(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    e1 = EdgeSet.from_iter(values, directed=directed)

    random.shuffle(values)
    e2 = EdgeSet.from_iter(values, directed=(not directed))

    assert e1 != e2


@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_equal_when_edgesets_has_different_sizes(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    e1 = EdgeSet.from_iter(values, directed=directed)

    random.shuffle(values)
    e2 = EdgeSet.from_iter(values, directed=directed)

    assert e1 == e2
    e2.pop()
    assert e1 != e2

@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_equal_when_remove_the_same_element(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    e1 = EdgeSet.from_iter(values, directed=directed)

    random.shuffle(values)
    e2 = EdgeSet.from_iter(values, directed=directed)

    assert e1 == e2
    e1.remove(e2.pop())
    assert e1 == e2

@pytest.mark.parametrize(
    "n_items, directed, weighted",
    [(100, True, True), (100, True, False),
     (100, False, True), (100, False, False)]
)
def test_equal_when_copy_edges(n_items, directed, weighted):

    values = [ gen_values(weighted) for _ in range(n_items)]
    e1 = EdgeSet.from_iter(values, directed=directed)

    e2 = e1.copy()

    assert e1 is not e2
    assert e1 == e2