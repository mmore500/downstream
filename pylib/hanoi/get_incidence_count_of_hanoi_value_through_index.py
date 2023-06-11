def get_incidence_count_of_hanoi_value_through_index(value: int, n: int) -> int:
    """How many times has the hanoi value value occured at indices up to and including index n?

    See `get_hanoi_value_at_index` for notes on zero-based variant of Hanoi sequence used.
    """
    offset = 2**value - 1
    cadence = 2 ** (value + 1)
    return (n - offset + cadence) // cadence
