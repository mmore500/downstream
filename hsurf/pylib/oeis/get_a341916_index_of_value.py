from ..bit_encode_gray import bit_encode_gray
from .get_a059893_index_of_value import get_a059893_index_of_value


def get_a341916_index_of_value(n: int) -> int:
    # https://oeis.org/A341916
    return get_a059893_index_of_value(bit_encode_gray(n)) + 1
