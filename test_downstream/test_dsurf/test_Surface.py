import types
import typing

import pytest

from downstream.dstream import steady_algo, stretched_algo, tilted_algo
from downstream.dsurf import Surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface(algo: types.ModuleType, S: int) -> None:
    surface = Surface(algo, S)
    assert surface.T == 0
    assert [*surface] == [None] * S
    assert [*surface.lookup()] == [None] * S

    for T in range(100):
        site = surface.ingest(T)
        if site is not None:
            assert surface[site] == T
        assert [*surface] == [*surface.lookup()]
        assert [*zip(surface.lookup(), surface)] == [*surface.enumerate()]


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface_ingest_many(algo: types.ModuleType, S: int) -> None:
    single_surface = Surface(algo, S)
    multi_surface = Surface(algo, S)
    for T in range(int((algo.get_ingest_capacity(S) or 10000) ** 0.2)):
        single_sites: typing.List[typing.Optional[int]] = [None] * S
        for _ in range(T):
            site = single_surface.ingest(T)
            if site is not None:
                single_sites[site] = single_surface.T - 1
        multi_sites = multi_surface.ingest_multiple(T, lambda _: T)
        assert [
            (site, timestamp)
            for site, timestamp in enumerate(single_sites)
            if timestamp is not None
        ] == multi_sites
        assert multi_surface.T == single_surface.T
        assert [*single_surface] == [*multi_surface]
        assert [*single_surface.enumerate()] == [*multi_surface.enumerate()]
