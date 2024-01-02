from ......pylib import hanoi
from ._calc_incidence_of_deposited_hanoi_value import (
    calc_incidence_of_deposited_hanoi_value,
)


def calc_rank_of_deposited_hanoi_value(
    hanoi_value: int,
    reservation_index: int,
    surface_size: int,
    focal_rank: int,
) -> int:
    """What deposition rank is resident at the surface site associated with the
    `reservation_index` semantic position of `hanoi_value`'s reservation
    incidence buffer?

    Requires query params refer to a `reservation_index` that has been reached
    by deposited incidences and a `reservation_index` is still present at
    `focal_rank`.
    """
    incidence = calc_incidence_of_deposited_hanoi_value(
        hanoi_value,
        reservation_index,
        surface_size,
        focal_rank,
    )
    res = hanoi.get_index_of_hanoi_value_nth_incidence(hanoi_value, incidence)
    assert res <= focal_rank, {
        "hanoi_value": hanoi_value,
        "incidence": incidence,
        "focal_rank": focal_rank,
        "res": res,
        "reservation_index": reservation_index,
        "surface_size": surface_size,
    }
    return res
