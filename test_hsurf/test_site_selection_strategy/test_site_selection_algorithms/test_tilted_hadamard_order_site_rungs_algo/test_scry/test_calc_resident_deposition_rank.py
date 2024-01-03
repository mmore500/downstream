import typing

import pytest

from hsurf.hsurf import tilted_hadamard_order_site_rungs_algo as algo
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_surface_rank_capacity,
)


def test_calc_resident_deposition_rank_unit():
    assert [
        algo.calc_resident_deposition_rank(0, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        0,  # 1,  # 4,  # 1,  # 1
        0,  # 8,  # 4,  # 0,  # 2
        0,  # 2,  # 4,  # 2,  # 3
        0,  # 12, # 4,  # 0,  # 4
        0,  # 9,  # 4,  # 1,  # 5
        0,  # 4,  # 4,  # 0,  # 6
        0,  # 3,  # 4,  # 3,  # 7
        8,  # 0,  # 4,  # 0,  # 8
        8,  # 13  # 4,  # 1,  # 9
        8,  # 8,  # 2,  # 0,  # 10
        8,  # 10, # 2,  # 2,  # 11
        12, # 0,  # 2,  # 0,  # 12
        12, # 5,  # 2,  # 1,  # 13
        12, # 8,  # 2,  # 0,  # 14
        12, # 4,  # 2,  # 4,  # 15
        16, # 0,  # 2,  # 0,  # 16
        16, # 1,  # 2,  # 1,  # 17
        16, # 8,  # 2,  # 0,  # 18
        16, # 14  # 2,  # 2,  # 19
        20, # 0,  # 2,  # 0,  # 20
        20,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        algo.calc_resident_deposition_rank(1, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        1,  # 1,  # 4,  # 1,  # 1
        1,  # 8,  # 4,  # 0,  # 2
        1,  # 2,  # 4,  # 2,  # 3
        1,  # 12, # 4,  # 0,  # 4
        1,  # 9,  # 4,  # 1,  # 5
        1,  # 4,  # 4,  # 0,  # 6
        1,  # 3,  # 4,  # 3,  # 7
        1,  # 0,  # 4,  # 0,  # 8
        1,  # 13  # 4,  # 1,  # 9
        1,  # 8,  # 2,  # 0,  # 10
        1,  # 10, # 2,  # 2,  # 11
        1,  # 0,  # 2,  # 0,  # 12
        1,  # 5,  # 2,  # 1,  # 13
        1,  # 8,  # 2,  # 0,  # 14
        1,  # 4,  # 2,  # 4,  # 15
        1,  # 0,  # 2,  # 0,  # 16
        17, # 1,  # 2,  # 1,  # 17
        17, # 8,  # 2,  # 0,  # 18
        17, # 14  # 2,  # 2,  # 19
        17, # 0,  # 2,  # 0,  # 20
        17,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        algo.calc_resident_deposition_rank(2, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        0,  # 1,  # 4,  # 1,  # 1
        0,  # 8,  # 4,  # 0,  # 2
        3,  # 2,  # 4,  # 2,  # 3
        3,  # 12, # 4,  # 0,  # 4
        3,  # 9,  # 4,  # 1,  # 5
        3,  # 4,  # 4,  # 0,  # 6
        3,  # 3,  # 4,  # 3,  # 7
        3,  # 0,  # 4,  # 0,  # 8
        3,  # 13  # 4,  # 1,  # 9
        3,  # 8,  # 2,  # 0,  # 10
        3,  # 10, # 2,  # 2,  # 11
        3,  # 0,  # 2,  # 0,  # 12
        3,  # 5,  # 2,  # 1,  # 13
        3,  # 8,  # 2,  # 0,  # 14
        3,  # 4,  # 2,  # 4,  # 15
        3,  # 0,  # 2,  # 0,  # 16
        3,  # 1,  # 2,  # 1,  # 17
        3,  # 8,  # 2,  # 0,  # 18
        3,  # 14  # 2,  # 2,  # 19
        3,  # 0,  # 2,  # 0,  # 20
        3,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        algo.calc_resident_deposition_rank(15, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        0,  # 1,  # 4,  # 1,  # 1
        0,  # 8,  # 4,  # 0,  # 2
        0,  # 2,  # 4,  # 2,  # 3
        0,  # 12, # 4,  # 0,  # 4
        0,  # 9,  # 4,  # 1,  # 5
        0,  # 4,  # 4,  # 0,  # 6
        0,  # 3,  # 4,  # 3,  # 7
        0,  # 0,  # 4,  # 0,  # 8
        0,  # 13  # 4,  # 1,  # 9
        0,  # 8,  # 2,  # 0,  # 10
        0,  # 10, # 2,  # 2,  # 11
        0,  # 0,  # 2,  # 0,  # 12
        0,  # 5,  # 2,  # 1,  # 13
        0,  # 8,  # 2,  # 0,  # 14
        0,  # 4,  # 2,  # 4,  # 15
        0,  # 0,  # 2,  # 0,  # 16
        0,  # 1,  # 2,  # 1,  # 17
        0,  # 8,  # 2,  # 0,  # 18
        0,  # 14  # 2,  # 2,  # 19
        0,  # 0,  # 2,  # 0,  # 20
        0,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        algo.calc_resident_deposition_rank(8, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        0,  # 1,  # 4,  # 1,  # 1
        2,  # 8,  # 4,  # 0,  # 2
        2,  # 2,  # 4,  # 2,  # 3
        2,  # 12, # 4,  # 0,  # 4
        2,  # 9,  # 4,  # 1,  # 5
        2,  # 4,  # 4,  # 0,  # 6
        2,  # 3,  # 4,  # 3,  # 7
        2,  # 0,  # 4,  # 0,  # 8
        2,  # 13  # 4,  # 1,  # 9
        10, # 8,  # 2,  # 0,  # 10
        10, # 10, # 2,  # 2,  # 11
        10, # 0,  # 2,  # 0,  # 12
        10, # 5,  # 2,  # 1,  # 13
        14, # 8,  # 2,  # 0,  # 14
        14, # 4,  # 2,  # 4,  # 15
        14, # 0,  # 2,  # 0,  # 16
        14, # 1,  # 2,  # 1,  # 17
        18, # 8,  # 2,  # 0,  # 18
        18, # 14  # 2,  # 2,  # 19
        18, # 0,  # 2,  # 0,  # 20
        18,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        algo.calc_resident_deposition_rank(9, 16, num_depositions)
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        0,  # ~~~~ n/a ~~~~
        0,  # 0,  # 8 , # 0,  # 0
        0,  # 1,  # 4,  # 1,  # 1
        0,  # 8,  # 4,  # 0,  # 2
        0,  # 2,  # 4,  # 2,  # 3
        0,  # 12, # 4,  # 0,  # 4
        5,  # 9,  # 4,  # 1,  # 5
        5,  # 4,  # 4,  # 0,  # 6
        5,  # 3,  # 4,  # 3,  # 7
        5,  # 0,  # 4,  # 0,  # 8
        5,  # 13  # 4,  # 1,  # 9
        5,  # 8,  # 2,  # 0,  # 10
        5,  # 10, # 2,  # 2,  # 11
        5,  # 0,  # 2,  # 0,  # 12
        5,  # 5,  # 2,  # 1,  # 13
        5,  # 8,  # 2,  # 0,  # 14
        5,  # 4,  # 2,  # 4,  # 15
        5,  # 0,  # 2,  # 0,  # 16
        5,  # 1,  # 2,  # 1,  # 17
        5,  # 8,  # 2,  # 0,  # 18
        5,  # 14  # 2,  # 2,  # 19
        5,  # 0,  # 2,  # 0,  # 20
        21,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]


@pytest.mark.parametrize(
    "surface_size",
    [2**x for x in range(2, 6)]
    + [pytest.param(2**x, marks=pytest.mark.heavy) for x in range(6, 11)],
)
@pytest.mark.parametrize(
    "num_generations_bidder",
    [
        lambda surface_size: 2**14 // surface_size,
        pytest.param(
            lambda surface_size: 2**18 // max(1, surface_size >> 9),
            marks=pytest.mark.heavy,
        ),
    ],
)
def test_calc_resident_deposition_rank_integration(
    surface_size: int,
    num_generations_bidder: typing.Callable,
):
    num_generations = min(
        num_generations_bidder(surface_size),
        get_surface_rank_capacity(surface_size) - 1,
    )
    surface_deposition_ranks = [0] * surface_size
    for rank in range(num_generations):
        target_site = algo.pick_deposition_site(rank, surface_size)
        surface_deposition_ranks[target_site] = rank

        for site, actual_deposition_rank in enumerate(
            surface_deposition_ranks
        ):
            calculated_deposition_rank = algo.calc_resident_deposition_rank(
                site,
                surface_size,
                rank + 1,
            )
            assert calculated_deposition_rank == actual_deposition_rank, {
                "actual deposition rank": actual_deposition_rank,
                "calculated deposition rank": calculated_deposition_rank,
                "num depositions": rank + 1,
                "rank": rank,
                "site": site,
            }
