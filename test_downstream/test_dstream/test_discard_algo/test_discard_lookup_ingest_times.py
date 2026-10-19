import pytest

from downstream.dstream import discard_algo as algo


@pytest.mark.parametrize("S", [1, 2, 3, 4, 5, 8, 16, 17, 100])
def test_discard_time_lookup(S: int):
    for T in [*range(S * 4), 2**64]:
        assert [*algo.lookup_ingest_times(S, T)] == [None] * S
