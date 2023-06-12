def get_longeveity_ordered_position(i: int, num_items: int) -> int:
    longeveity_depth = (window_idx + 1).bit_length() - 1
    longeveity_offset = num_windows // 2**longeveity_depth
    longeveity_spacing = longeveity_offset * 2
    longeveity_ordered_window_idx = (
        longeveity_offset
        + longeveity_spacing * pylib.get_powersof2triangle_val_at_index(window_idx)
    )
