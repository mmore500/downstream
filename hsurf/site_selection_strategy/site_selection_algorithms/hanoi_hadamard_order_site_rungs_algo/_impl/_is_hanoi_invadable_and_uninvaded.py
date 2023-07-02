from ._is_hanoi_invaded import is_hanoi_invaded
from ._is_hanoi_invader import is_hanoi_invader


def is_hanoi_invadable_and_uninvaded(hanoi_value: int, rank: int) -> bool:
    """Will `hanoi_value` have its incidence reservation buffer size halved
    during the current reservation-size-doubling cycle, but has not had any
    sites overwritten by an invading hanoi value during the current cycle?"""
    return not is_hanoi_invader(hanoi_value, rank) and not is_hanoi_invaded(
        hanoi_value, rank
    )
