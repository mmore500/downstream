from .....pylib import bit_count_immediate_zeros


def get_nth_bin_width(n: int, surface_size: int) -> int:
    # the width of a bin controls how many distinct hanoi value it holds
    # before it is full and the subsequent hanoi value wraps around to overwrite
    # the lowest held hanoi value
    # entries from a single hanoi value are stored in sequential bins, one
    # per bin
    # earlier bins have higher widths because high-hanoi value entries are
    # observed slower than low-hanoi value entries
    #
    # the number of bins with a particular width doubles with each width step
    # (except for the first step, where no change occurs)
    # and the width decreases by one per step
    #
    # this particular set of bin widths is based on how the distribution of
    # hanoi value counts as a surface fils up for the first time
    # below, >> 1 is equivalent to // 2
    return bit_count_immediate_zeros(n + (surface_size >> 1)) + 1
