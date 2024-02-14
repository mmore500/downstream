def bit_encode_gray(n: int) -> int:
    """Encode an integer using Gray code.

    Gray code is a binary numeral system where two successive values differ in
    only one bit. See <https://en.wikipedia.org/wiki/Gray_code>.
    """
    return n ^ (n >> 1)
