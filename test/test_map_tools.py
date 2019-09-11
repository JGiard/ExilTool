from exiltool.map.tools import compute_prod


def test_compute_prod():
    assert compute_prod(80, 60) == 9438
