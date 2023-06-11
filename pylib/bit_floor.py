def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    # adapted from https://github.com/mmore500/hstrat/blob/e9c2994c7a6514162f1ab685d88c374372dc1cf0/hstrat/_auxiliary_lib/_bit_floor.py
    if n:
        # see https://stackoverflow.com/a/14267825/17332200
        exp = (n // 2).bit_length()
        res = 1 << exp
        return res
    else:
        return 0
