def get_index_of_hanoi_value_nth_incidence(value: int, n: int) -> int:
    """At what index does the nth incidence of a given value occur within the
    Hanoi sequence?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    offset = 2**value - 1
    cadence = 2 ** (value + 1)
    return offset + cadence * n
