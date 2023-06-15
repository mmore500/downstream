from ..bit_drop_msb import bit_drop_msb
from ..bit_floor import bit_floor
from ..bit_reverse import bit_reverse


def get_a059893_value_at_index(n: int) -> int:
    # https://oeis.org/A059893
    return int('1' + bin(n + 1)[3:][::-1], 2)
