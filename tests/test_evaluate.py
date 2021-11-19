import random

from edgesets import EdgeSet, UEdge
from edgesets.evaluation import EvaluateEdgeSet


def test_evaluate_unweighted_edgeset():

    chromossome = EdgeSet()

    x = random.choice(range(1_000, 10_000))

    for _ in range(x):
        a = random.randint(0, 10_000)
        b = random.randint(0, 10_000)
        if a != b:
            chromossome.add(UEdge(a, b))

    evaluator = EvaluateEdgeSet()
    total = evaluator(chromossome)
    assert total == len(chromossome)

def test_evaluate_weighted_edgeset():

    chromossome = EdgeSet()

    x = random.choice(range(1_000, 10_000))
    weights = list()
    for _ in range(x):
        a = random.randint(0, 10_000)
        b = random.randint(0, 10_000)
        if a != b:
            # w = random.randint(1, 100_000)
            w = random.random() * 10
            weights.append(w)
            chromossome.add(UEdge(a, b, weight=w))

    evaluator = EvaluateEdgeSet()
    total = evaluator(chromossome)
    assert round(total, ndigits=2) == round(sum(weights), ndigits=2)
