from .get_incidence_count_of_hanoi_value_through_index import (
    get_incidence_count_of_hanoi_value_through_index,
)
from .get_index_of_hanoi_value_nth_incidence import (
    get_index_of_hanoi_value_nth_incidence,
)


def get_index_of_hanoi_value_next_incidence(value: int, index: int) -> int:
    """At what index does the next incidence of a given value occur within the
    Hanoi sequence past the given index?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    incidence_count = get_incidence_count_of_hanoi_value_through_index(
        value,
        index,
    )
    # note: implicit +1 in converting from count to incidence index
    return get_index_of_hanoi_value_nth_incidence(value, incidence_count)
