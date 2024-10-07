import functools
import typing

from downstream.stretched_algo import site_selection
from downstream.stretched_algo import time_lookup as time_lookup_


def validate_stretched_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[typing.Optional[int]]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
            yield v

    return wrapper


time_lookup = validate_stretched_time_lookup(time_lookup_)


def test_stretched_time_lookup_against_site_selection():
    for s in range(1, 12):
        S = 1 << s
        T_max = min(1 << 17 - s, 2**S - 1)
        expected = [None] * S
        for T in range(T_max):
            actual = time_lookup(S, T)
            assert all(x == y for x, y in zip(expected, actual))

            site = site_selection(S, T)
            if site is not None:
                expected[site] = T
