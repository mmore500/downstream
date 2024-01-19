def bit_decode_gray(n: int) -> int:
    x = n
    e = 1
    while x:
        x = n >> e
        e <<= 1
        n ^= x
    return n
