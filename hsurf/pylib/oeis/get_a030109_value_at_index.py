from ..bit_reverse import bit_reverse


def get_a030109_value_at_index(n: int) -> int:
    # https://oeis.org/A030109
    return (bit_reverse(n + 1) - 1) // 2
