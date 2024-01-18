from ..bit_floor import bit_floor
from ..hanoi import (
    get_hanoi_value_at_index,
    get_hanoi_value_incidence_at_index,
)


def get_a130654_value_at_index(n: int) -> int:
    # https://oeis.org/A130654
    assert n > 0  # 1-indexed
    rebased = n - bit_floor(n) - 1
    if rebased < 0:
        return 0
    assert rebased >= 0
    hanoi_value = get_hanoi_value_at_index(rebased)
    hanoi_incidence = get_hanoi_value_incidence_at_index(rebased)
    return min(hanoi_value, hanoi_incidence.bit_count()) + 1
