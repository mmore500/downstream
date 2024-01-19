from .get_a000295_value_at_index import get_a000295_value_at_index


# see https://oeis.org/A000295
def get_a000295_index_of_value(v: int) -> int:
    """Return the greatest index of A000295 with value `<= v`.

    Note: uses -1 as the first index, i.e., skips zeroth element.
    """
    ansatz = (v + 1).bit_length() - 1
    correction = get_a000295_value_at_index(ansatz) > v
    return ansatz - correction
