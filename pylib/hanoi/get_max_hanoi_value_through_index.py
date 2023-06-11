from ..bit_ceil import bit_ceil
from ..bit_floor import bit_floor


def get_max_hanoi_value_through_index(n: int) -> int:
    """What is the largest hanoi value that occurs at indices up to and
    including index n?

    See `get_hanoi_value_at_index` for notes on zero-based variant of Hanoi sequence used.
    """
    # offset = 2**value - 1
    # offset + 1 = 2**value
    # floorlog2(offset + 1) = value
    return (n + 1).bit_length() - 1
