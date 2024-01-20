from ..oeis import get_a025480_value_at_index


def get_longevity_index_of_mapped_position(
    index: int, num_indices: int
) -> int:
    assert num_indices.bit_count() == 1
    grundy_offset = num_indices - 1
    return get_a025480_value_at_index(grundy_offset + index)
