# see https://oeis.org/A000295
def get_a000295_value_at_index(n: int) -> int:
    """Return the value of A000295 at the given index.

    Note: uses -1 as the first index, i.e., skips zeroth element.
    """
    n += 1
    return (1 << n) - n - 1
