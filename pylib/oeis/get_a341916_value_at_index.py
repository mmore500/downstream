from ..bit_decode_gray import bit_decode_gray
from .get_a059893_value_at_index import get_a059893_value_at_index


def get_a341916_value_at_index(n: int) -> int:
    # https://oeis.org/A341916
    return bit_decode_gray(get_a059893_value_at_index(n - 1))
