from ..bit_reverse import bit_reverse


def get_a030109_index_of_value(
    value: int,
    index_plus_one_bit_length: int,
) -> int:
    # https://oeis.org/A030109
    j = bit_reverse(value * 2 + 1)
    assert index_plus_one_bit_length >= j.bit_length()
    k = j << (index_plus_one_bit_length - j.bit_length())
    assert k.bit_length() == index_plus_one_bit_length
    return k - 1
