def get_longevity_level_of_mapped_position(
    mapped_position: int,
    num_positions: int,
) -> int:
    least_significant_set_bit = (
        mapped_position & -mapped_position
    ).bit_length()
    return (
        0
        if mapped_position == 0
        else (num_positions.bit_length() - least_significant_set_bit)
    )
