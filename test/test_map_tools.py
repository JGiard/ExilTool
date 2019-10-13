from exiltool.map.tools import compute_prod


def test_compute_prod():
    assert compute_prod(80, 60) == 14321
    assert compute_prod(120, 150) == 58226
