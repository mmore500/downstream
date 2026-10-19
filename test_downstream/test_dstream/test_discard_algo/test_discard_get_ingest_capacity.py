from downstream.dstream import discard_algo as algo


def test_discard_get_ingest_capacity():
    assert algo.get_ingest_capacity(0) == 0
    for S in range(1, 17):
        assert algo.get_ingest_capacity(S) is None
