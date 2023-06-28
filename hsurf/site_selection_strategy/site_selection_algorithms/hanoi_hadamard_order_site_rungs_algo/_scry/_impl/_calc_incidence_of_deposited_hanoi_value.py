from ......pylib import hanoi
from ..._impl._get_num_reservations_provided import (
    get_num_reservations_provided,
)
from ._calc_reservation_reference_incidence import (
    calc_reservation_reference_incidence,
)


def calc_incidence_of_deposited_hanoi_value(
    hanoi_value: int,
    reservation_index: int,
    surface_size: int,
    focal_rank: int,
    _is_recurse=False,  # TODO refactor away debugging param
) -> int:
    num_reservations_provided = get_num_reservations_provided(
        hanoi_value=hanoi_value,
        surface_size=surface_size,
        rank=focal_rank,
    )
    assert num_reservations_provided

    assert reservation_index < num_reservations_provided, {
        "num_reservations_provided": num_reservations_provided,
        "reservation_index": reservation_index,
    }

    focal_count = hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, focal_rank
    )
    assert focal_count

    focal_incidence = focal_count - 1
    # this case (not enough deposits to reach reservation)
    # is handled elsewhere before this fn
    assert focal_incidence >= reservation_index

    # figure out where the modulus lines up at the zero position
    reference_incidence = calc_reservation_reference_incidence(
        hanoi_value=hanoi_value,
        reservation_index=reservation_index,
        surface_size=surface_size,
        focal_rank=focal_rank,
    )
    assert reference_incidence >= 0

    assert focal_incidence >= reference_incidence

    incidence_duration = focal_incidence - reference_incidence
    assert incidence_duration >= reservation_index

    res = reference_incidence + reservation_index
    assert res <= focal_incidence, {
        "res": res,
        "focal_incidence": focal_incidence,
        "reference incidence": reference_incidence,
        "reservation index": reservation_index,
    }  # make sure incidence has actually occured
    return res
