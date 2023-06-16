from .get_a059893_value_at_index import get_a059893_value_at_index


def get_a059893_index_of_value(n: int) -> int:
    # own inverse
    return get_a059893_value_at_index(n - 1) - 1
