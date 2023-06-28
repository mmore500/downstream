import pytest

from hsurf import hanoi_hadamard_order_site_rungs_algo as algo


@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_select_deposit_site_smoke(surface_size: int, rank: int) -> int:
    # just a smoke test
    deposit_site = algo.select_deposit_site(rank, surface_size)
    assert isinstance(deposit_site, int)
    assert 0 <= deposit_site < surface_size
