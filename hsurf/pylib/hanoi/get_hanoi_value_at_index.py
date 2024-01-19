def get_hanoi_value_at_index(n: int) -> int:
    """Get value of zero-indexed, zero-based Hanoi sequence in constant time.

    This sequence is [A007814](https://oeis.org/A007814) in the Online
    Encyclopedia of Integer Sequences. Equivalent to the Hanoi sequence
    ([A001511](https://oeis.org/A00151)), with all values less one. Indexing
    assumes zero-based convention.
    """
    n += 1
    return (n & -n).bit_length() - 1
