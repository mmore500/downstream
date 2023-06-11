from .get_hanoi_value_at_index import get_hanoi_value_at_index


def get_hanoi_value_incidence_at_index(n: int) -> int:
    """How many times has the hanoi value at index n already been encountered?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    return n // 2 ** (get_hanoi_value_at_index(n) + 1)
