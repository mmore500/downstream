from ..bit_floor import bit_floor
from ..bit_reverse import bit_reverse


def get_a059893_value_at_index(n: int) -> int:
    # https://oeis.org/A059893
    return bit_floor(n + 1) | (bit_reverse(n + 1) >> 1)
