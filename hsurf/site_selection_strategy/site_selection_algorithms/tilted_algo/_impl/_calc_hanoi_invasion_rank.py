from .....pylib import hanoi
from ._calc_invading_hanoi_value import calc_invading_hanoi_value


def calc_hanoi_invasion_rank(
    hanoi_value: int, epoch: int, surface_size: int
) -> int:
    """At the rank will the reservation for `hanoi_value` be shrunk?"""
    invader = calc_invading_hanoi_value(hanoi_value, epoch, surface_size)
    return hanoi.get_hanoi_value_index_offset(invader)
