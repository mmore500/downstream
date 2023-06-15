from .get_hanoi_value_index_cadence import get_hanoi_value_index_cadence
from .get_hanoi_value_index_offset import get_hanoi_value_index_offset


def get_index_of_hanoi_value_nth_incidence(value: int, n: int) -> int:
    """At what index does the nth incidence of a given value occur within the
    Hanoi sequence?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    offset = get_hanoi_value_index_offset(value)
    cadence = get_hanoi_value_index_cadence(value)
    return offset + cadence * n
