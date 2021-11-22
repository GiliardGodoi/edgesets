from edgesets import UEdge, DEdge

def test_repr():
    e1 = DEdge(7, 8)
    text = repr(e1)
    assert text == "DEdge(7, 8, weight=1)"

    e2 = eval(text)
    assert type(e1) == type(e1)
    assert e1 == e2

def test_if_directions_are_differents_with_same_nodes():
    d1 = DEdge(10, 15)
    d2 = DEdge(15, 10)
    assert d1 != d2
    assert hash(d1) != hash(d2)

def test_if_DEdge_is_differente_from_UEdge():
    d1 = DEdge(10, 15)
    d2 = UEdge(15, 10)

    assert d1 != d2
    assert hash(d1) != hash(d2)


def test_DEdge_is_different_from_tuple():
    param = (25, 42)
    edge = DEdge(*param)
    assert edge != param
    assert hash(edge) != hash(param)

def test_DEdge_is_different_from_list():
    param = [24, 25]
    edge = DEdge(*param)
    assert edge != param
    # assert hash(edge) != hash(param) # list is not hashable