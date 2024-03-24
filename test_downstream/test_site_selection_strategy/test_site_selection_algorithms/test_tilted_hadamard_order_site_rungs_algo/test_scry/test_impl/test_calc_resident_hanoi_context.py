import typing

import opytional as opyt
import pytest

from downstream.downstream import tilted_hadamard_order_site_rungs_algo as algo
from downstream.pylib import hanoi
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_surface_rank_capacity,
)
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._scry._impl import (
    calc_resident_hanoi_context,
)


def test_calc_resident_hanoi_context_smoke():
    assert calc_resident_hanoi_context(0, 16, 0) is None
    assert all(
        key in calc_resident_hanoi_context(0, 16, 1)
        for key in ("hanoi value", "reservation index", "focal rank")
    )


def test_calc_resident_hanoi_context_unit():
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(0, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
            # deposition site
            #     # num_reservations
            #     #     # hanoi sequence (0-based):
            #     #     #     rank
        None,  # ~~~~ n/a ~~~~
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
        opyt.apply_if(
            calc_resident_hanoi_context(1, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        1,     # 1,  # 4,  # 1,  # 1
        1,     # 8,  # 4,  # 0,  # 2
        1,     # 2,  # 4,  # 2,  # 3
        1,     # 12, # 4,  # 0,  # 4
        1,     # 9,  # 4,  # 1,  # 5
        1,     # 4,  # 4,  # 0,  # 6
        1,     # 3,  # 4,  # 3,  # 7
        1,     # 0,  # 4,  # 0,  # 8
        1,     # 13  # 4,  # 1,  # 9
        1,     # 8,  # 2,  # 0,  # 10
        1,     # 10, # 2,  # 2,  # 11
        1,     # 0,  # 2,  # 0,  # 12
        1,     # 5,  # 2,  # 1,  # 13
        1,     # 8,  # 2,  # 0,  # 14
        1,     # 4,  # 2,  # 4,  # 15
        1,     # 0,  # 2,  # 0,  # 16
        1,     # 1,  # 2,  # 1,  # 17
        1,     # 8,  # 2,  # 0,  # 18
        1,     # 14  # 2,  # 2,  # 19
        1,     # 0,  # 2,  # 0,  # 20
        1,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(2, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        None,  # 1,  # 4,  # 1,  # 1
        None,  # 8,  # 4,  # 0,  # 2
        2,     # 2,  # 4,  # 2,  # 3
        2,     # 12, # 4,  # 0,  # 4
        2,     # 9,  # 4,  # 1,  # 5
        2,     # 4,  # 4,  # 0,  # 6
        2,     # 3,  # 4,  # 3,  # 7
        2,     # 0,  # 4,  # 0,  # 8
        2,     # 13  # 4,  # 1,  # 9
        2,     # 8,  # 2,  # 0,  # 10
        2,     # 10, # 2,  # 2,  # 11
        2,     # 0,  # 2,  # 0,  # 12
        2,     # 5,  # 2,  # 1,  # 13
        2,     # 8,  # 2,  # 0,  # 14
        2,     # 4,  # 2,  # 4,  # 15
        2,     # 0,  # 2,  # 0,  # 16
        2,     # 1,  # 2,  # 1,  # 17
        2,     # 8,  # 2,  # 0,  # 18
        2,     # 14  # 2,  # 2,  # 19
        2,     # 0,  # 2,  # 0,  # 20
        2,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(15, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        None,  # 1,  # 4,  # 1,  # 1
        None,  # 8,  # 4,  # 0,  # 2
        None,  # 2,  # 4,  # 2,  # 3
        None,  # 12, # 4,  # 0,  # 4
        None,  # 9,  # 4,  # 1,  # 5
        None,  # 4,  # 4,  # 0,  # 6
        None,  # 3,  # 4,  # 3,  # 7
        None,  # 0,  # 4,  # 0,  # 8
        None,  # 13  # 4,  # 1,  # 9
        None,  # 8,  # 2,  # 0,  # 10
        None,  # 10, # 2,  # 2,  # 11
        None,  # 0,  # 2,  # 0,  # 12
        None,  # 5,  # 2,  # 1,  # 13
        None,  # 8,  # 2,  # 0,  # 14
        None,  # 4,  # 2,  # 4,  # 15
        None,  # 0,  # 2,  # 0,  # 16
        None,  # 1,  # 2,  # 1,  # 17
        None,  # 8,  # 2,  # 0,  # 18
        None,  # 14  # 2,  # 2,  # 19
        None,  # 0,  # 2,  # 0,  # 20
        None,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(8, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        None,  # 1,  # 4,  # 1,  # 1
        0,     # 8,  # 4,  # 0,  # 2
        0,     # 2,  # 4,  # 2,  # 3
        0,     # 12, # 4,  # 0,  # 4
        0,     # 9,  # 4,  # 1,  # 5
        0,     # 4,  # 4,  # 0,  # 6
        0,     # 3,  # 4,  # 3,  # 7
        0,     # 0,  # 4,  # 0,  # 8
        0,     # 13  # 4,  # 1,  # 9
        0,     # 8,  # 2,  # 0,  # 10
        0,     # 10, # 2,  # 2,  # 11
        0,     # 0,  # 2,  # 0,  # 12
        0,     # 5,  # 2,  # 1,  # 13
        0,     # 8,  # 2,  # 0,  # 14
        0,     # 4,  # 2,  # 4,  # 15
        0,     # 0,  # 2,  # 0,  # 16
        0,     # 1,  # 2,  # 1,  # 17
        0,     # 8,  # 2,  # 0,  # 18
        0,     # 14  # 2,  # 2,  # 19
        0,     # 0,  # 2,  # 0,  # 20
        0,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(9, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        None,  # 1,  # 4,  # 1,  # 1
        None,  # 8,  # 4,  # 0,  # 2
        None,  # 2,  # 4,  # 2,  # 3
        None,  # 12, # 4,  # 0,  # 4
        1,     # 9,  # 4,  # 1,  # 5
        1,     # 4,  # 4,  # 0,  # 6
        1,     # 3,  # 4,  # 3,  # 7
        1,     # 0,  # 4,  # 0,  # 8
        1,     # 13  # 4,  # 1,  # 9
        1,     # 8,  # 2,  # 0,  # 10
        1,     # 10, # 2,  # 2,  # 11
        1,     # 0,  # 2,  # 0,  # 12
        1,     # 5,  # 2,  # 1,  # 13
        1,     # 8,  # 2,  # 0,  # 14
        1,     # 4,  # 2,  # 4,  # 15
        1,     # 0,  # 2,  # 0,  # 16
        1,     # 1,  # 2,  # 1,  # 17
        1,     # 8,  # 2,  # 0,  # 18
        1,     # 14  # 2,  # 2,  # 19
        1,     # 0,  # 2,  # 0,  # 20
        1,
        # 9,  # 2,  # 1,  # 21
        # fmt: on
    ]
    assert [
        opyt.apply_if(
            calc_resident_hanoi_context(4, 16, num_depositions),
            lambda x: x["hanoi value"],
        )
        for num_depositions in range(23)
    ] == [
        # fmt: off
               # deposition site
               #     # num_reservations
               #     #     # hanoi sequence (0-based):
               #     #     #     rank
        None,  # ~~~~ n/a ~~~~
        None,  # 0,  # 8 , # 0,  # 0
        None,  # 1,  # 4,  # 1,  # 1
        None,  # 8,  # 4,  # 0,  # 2
        None,  # 2,  # 4,  # 2,  # 3
        None,  # 12, # 4,  # 0,  # 4
        None,  # 9,  # 4,  # 1,  # 5
        0,     # 4,  # 4,  # 0,  # 6
        0,     # 3,  # 4,  # 3,  # 7
        0,     # 0,  # 4,  # 0,  # 8
        0,     # 13  # 4,  # 1,  # 9
        0,     # 8,  # 2,  # 0,  # 10
        0,     # 10, # 2,  # 2,  # 11
        0,     # 0,  # 2,  # 0,  # 12
        0,     # 5,  # 2,  # 1,  # 13
        0,     # 8,  # 2,  # 0,  # 14
        4,     # 4,  # 2,  # 4,  # 15
        4,     # 0,  # 2,  # 0,  # 16
        4,     # 1,  # 2,  # 1,  # 17
        4,     # 8,  # 2,  # 0,  # 18
        4,     # 14  # 2,  # 2,  # 19
        4,     # 0,  # 2,  # 0,  # 20
        4,
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
def test_calc_resident_hanoi_context_integration(
    surface_size: int,
    num_generations_bidder: typing.Callable,
):
    num_generations = min(
        num_generations_bidder(surface_size),
        get_surface_rank_capacity(surface_size),
    )
    surface_deposition_hanoi_values = [None] * surface_size
    for rank in range(num_generations):
        for site, actual_hanoi_value in enumerate(
            surface_deposition_hanoi_values
        ):
            calculated_hanoi_context = calc_resident_hanoi_context(
                site, surface_size, rank
            )
            assert (
                opyt.apply_if(
                    calculated_hanoi_context,
                    lambda x: x["hanoi value"],
                )
                == actual_hanoi_value
            )

        target_site = algo.pick_deposition_site(rank, surface_size)
        surface_deposition_hanoi_values[
            target_site
        ] = hanoi.get_hanoi_value_at_index(rank)
