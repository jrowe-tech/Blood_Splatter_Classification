from blob_utils import binary_range_search as brs

test = tuple(range(100))


def test_greater_than():
    results = brs(80, test)
    assert results == (80, 81)


def test_less_than():
    results = brs(20, test)
    assert results == (20, 21)


def test_mid():
    results = brs(49, test)
    assert results == (49, 50)


def test_right_end():
    results = brs(99, test)
    assert results == (99, None)


def test_left_end():
    results = brs(0, test)
    assert results == (0, 1)


def test_clamp_left():
    results = brs(-10, test)
    assert results == (None, 0)


def test_clamp_right():
    results = brs(110, test)
    assert results == (99, None)
