def bit_encode_gray(n: int) -> int:
    return n ^ (n >> 1)
