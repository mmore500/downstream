from ._get_nth_bin_width import get_nth_bin_width
from ._get_num_segments import get_num_segments


def get_nth_segment_position(n: int, surface_size: int) -> int:
    # with bin positions distributed per get_nth_bin_width, how many positions
    # over does the nth bin start?
    # this is the sum of the widths of all bins before the nth bin
    assert 0 <= n < get_num_segments(surface_size)

    if n == 0:
        return 0

    assert surface_size.bit_count() == 1  # assume perfect power of 2
    mbw = surface_size.bit_length() - 1  # max bin width, num trailing zeros
    assert mbw == get_nth_bin_width(0, surface_size)

    position = mbw  # special case the first one-bin segment
    mbw -= 1  # new largest bin width is one less than the first
    n -= 1  # we've handled one bin

    # https://www.wolframalpha.com/input?i=%5Csum_%7Bj%3D0%7D%5E%7Bb-1%7D+q+%5Ccdot+2%5Ej
    position += (1 << n) * mbw - mbw
    # equiv: cum += sum(mbw << j for j in range(n))

    # https://www.wolframalpha.com/input?i=-2+%28-1+%2B+2%5En%29+%2B+2%5En+n&assumption=%22ClashPrefs%22+-%3E+%7B%22Math%22%7D
    position -= n * (1 << n) - (1 << (n + 1)) + 2
    # equiv: cum -=  sum(j << j for j in range(ncs))

    return position
