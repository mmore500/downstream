from .get_hanoi_value_index_cadence import get_hanoi_value_index_cadence
from .get_hanoi_value_index_offset import get_hanoi_value_index_offset


def get_incidence_count_of_hanoi_value_through_index(
    value: int, n: int
) -> int:
    """How many times has the hanoi value value occured at indices up to and including index n?

    See `get_hanoi_value_at_index` for notes on zero-based variant of Hanoi sequence used.
    """
    offset = get_hanoi_value_index_offset(value)
    cadence = get_hanoi_value_index_cadence(value)
    return (n - offset + cadence) // cadence
