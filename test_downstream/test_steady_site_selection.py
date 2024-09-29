import functools
import itertools as it
from random import randrange as rand
import typing

from .steady_site_selection import bit_floor, ctz, steady_site_selection


def test_ctz():
    # fmt: off
    assert [*map(ctz, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]


def test_bit_floor():
    # fmt: off
    assert [*map(bit_floor, range(1, 17))] == [
        1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16
    ]


def validate_steady_site_selection(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert res is None or 0 <= res < S - 1  # Assert valid output
        return res

    return wrapper


site_selection = validate_steady_site_selection(steady_site_selection)


def test_steady_site_selection8():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 3, 2, 5, 4, 6, 0,  # T 0-7
        None, 5, None, 3, None, 6, None, 1,  # T 8-15
        None, None, None, 5, None, None, None, 4,  # T 16-23
        None, None, None, 6, None, None, None, 2,  # T 24-31
        None, None, None, None, None, None, None, 5 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection16():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 4, 2, 7, 5, 9, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        11, 8, 12, 6, 13, 10, 14, 0,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        None, 11, None  # T 16-18 --- hv 0,1,0
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection_fuzz():
    testS = (1 << s for s in range(33))
    testT = it.chain(range(10**5), (rand(2**128) for _ in range(10**5)))
    for S, T in it.product(testS, testT):
        site_selection(S, T)  # Validated via wrapper


def test_steady_site_selection_epoch0():
    for S in (1 << s for s in range(21)):
        actual = {site_selection(S, T) for T in range(S - 1)}
        expected = set(range(S - 1))
        assert actual == expected
