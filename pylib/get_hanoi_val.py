def get_hanoi_val(n: int) -> int:
    # https://oeis.org/A00151
    n += 1
    return (n&-n).bit_length()
