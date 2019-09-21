from exiltool.model.resa import Resa


def test_comparison():
    assert Resa('foo', 5, 4, 9) < Resa('bar', 5, 8, 1)


def test_sort():
    resas = [Resa('foo', 5, 4, 9), Resa('bar', 5, 1, 1)]

    assert sorted(resas) == [Resa('bar', 5, 1, 1), Resa('foo', 5, 4, 9)]
