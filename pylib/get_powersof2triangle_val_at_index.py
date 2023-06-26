from .bit_floor import bit_floor

def get_powersof2triangle_val_at_index(n: int) -> int:
    """Get value from end-to-end concatenation of binary orders of magnitude
    enumerations in constant time.

    This sequence is [A053645](https://oeis.org/A053645) in the Online
    Encyclopedia of Integer Sequences. Indexing assumes zero-based convention.
    """
    return n - bit_floor(n + 1) + 1
