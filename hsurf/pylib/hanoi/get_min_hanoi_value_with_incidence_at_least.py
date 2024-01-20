import typing

from ..bit_floor import bit_floor


def get_min_hanoi_value_with_incidence_at_least(
    n: int, index: int
) -> typing.Optional[int]:
    """What is the smallest hanoi value has ocurred at least n + 1 times?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used. Returns None if no hanoi
    value has ocurred n + 1 times.
    """

    # 2n + 1 allows the offset to be accounted for
    cadence_upper_bound = 2 * (index + 1) // (2 * n + 1)
    cadence = bit_floor(cadence_upper_bound)

    if cadence <= 1:
        return None
    elif cadence > 1:
        assert cadence.bit_length() >= 2
        return cadence.bit_length() - 2
    else:
        assert False
