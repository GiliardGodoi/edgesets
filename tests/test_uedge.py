
from edgesets import UEdge, DEdge

def test_repr():
    e1 = UEdge(4, 3)
    text = repr(e1)
    assert text == "UEdge(3, 4)"

    e2 = eval(text)
    assert type(e1) == type(e1)
    assert e1 == e2

def test_UEdge_is_different_from_DEdge():
    ue = UEdge(4, 5)
    de = DEdge(4, 5)
    assert ue != de
    assert hash(ue) != hash(de)

    ue = UEdge(5, 4)
    de = DEdge(4, 5)
    assert ue != de
    assert hash(ue) != hash(de)

def test_uedge_is_equal_regarding_to_nodes_orders():

    e1 = UEdge(10, 34)
    e2 = UEdge(34, 10)

    assert e1 == e2
    assert hash(e2) == hash(e1)

def test_uedge_is_different_from_tuple():
    param = (25, 42)
    edge = UEdge(*param)
    assert edge != param
    assert hash(edge) != hash(param)

def test_uedge_is_different_from_list():
    param = [24, 25]
    edge = UEdge(*param)
    assert edge != param
    # assert hash(edge) != hash(param) # list is not hashable