import interval_search as inch

from .get_a005187_value_at_index import get_a005187_value_at_index


# https://oeis.org/A005187
def get_a005187_index_of_value(n: int) -> int:
    """Get the index of the largest value of A005187 less than or equal to n."""
    return inch.doubling_search(
        lambda x: get_a005187_value_at_index(x + 1) > n,
    )
