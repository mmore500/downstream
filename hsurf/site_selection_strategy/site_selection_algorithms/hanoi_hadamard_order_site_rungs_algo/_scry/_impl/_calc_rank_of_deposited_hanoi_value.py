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
