from downstream.dstream import discard_algo as algo


def test_discard_get_ingest_capacity():
    for S in range(17):
        assert algo.get_ingest_capacity(S) is None
