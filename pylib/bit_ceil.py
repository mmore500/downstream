def bit_ceil(n: int) -> int:
    """Calculate the smallest power of 2 not smaller than n."""
    # adapted from https://github.com/mmore500/hstrat/blob/e9c2994c7a6514162f1ab685d88c374372dc1cf0/hstrat/_auxiliary_lib/_bit_ceil.py
    assert n >= 0
    if n:
        # see https://stackoverflow.com/a/14267825/17332200
        exp = (n - 1).bit_length()
        res = 1 << exp
        return res
    else:
        return 1
