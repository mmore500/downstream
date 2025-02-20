from copy import deepcopy
import types

import opytional as opyt
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
@pytest.mark.parametrize("step_size", [1, 5, 25, 50])
def test_Surface_ingest_many(
    algo: types.ModuleType, S: int, step_size: int
) -> None:
    single_surface = Surface(algo, S)
    multi_surface = Surface(algo, S)
    num_iterations = min(
        (
            opyt.apply_if_or_value(
                algo.get_ingest_capacity(S), lambda x: x // step_size // 2, 100
            ),
            100,
        )
    )
    for T in range(num_iterations):
        for _ in range(step_size):
            single_surface.ingest(T)
        multi_surface.ingest_multiple(step_size, lambda _: T)
        assert multi_surface.T == single_surface.T
        assert [*single_surface] == [*multi_surface]
        assert [*single_surface.enumerate()] == [*multi_surface.enumerate()]


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface_ingest_none(algo: types.ModuleType, S: int):
    surf = Surface(algo, S)
    for T in range(100):
        surf.ingest(T)
        new_surf = Surface(algo, deepcopy(surf._storage))
        new_surf.ingest_multiple(0, lambda _: None)
        assert [*new_surf] == [*surf]


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_raises(algo: types.ModuleType, S: int):
    cap = algo.get_ingest_capacity(S)
    if cap is None:
        return
    with pytest.raises(AssertionError):
        Surface(algo, S).ingest_multiple(cap + 1, lambda _: 1)
    s = Surface(algo, S)
    s.ingest_multiple(cap, lambda _: 1)
    with pytest.raises(AssertionError):
        s.ingest(1)
