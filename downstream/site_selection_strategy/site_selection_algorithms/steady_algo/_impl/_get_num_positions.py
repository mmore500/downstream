def get_num_positions(surface_size: int) -> int:
    """How many surface sites are made available to the surface update
    algorithm?"""
    # site 0 on actual surface is excluded
    return surface_size - 1
