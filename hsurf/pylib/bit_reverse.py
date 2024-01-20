# adapted from https://stackoverflow.com/a/37579581
def bit_reverse(n: int) -> int:
    assert n >= 0
    res = 0
    while n:
        res = (res << 1) + (n & 1)
        n >>= 1
    return res
