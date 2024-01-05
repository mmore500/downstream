from .....pylib import bit_floor
from ._get_num_bins import get_num_bins


def get_nth_bin_position(n: int, surface_size: int) -> int:
    # with bin positions distributed per get_nth_bin_width, how many positions
    # over does the nth bin start?
    # this is the sum of the widths of all bins before the nth bin
    assert 0 <= n < get_num_bins(surface_size)

    if n == 0:
        return 0

    assert surface_size.bit_count() == 1  # assume perfect power of 2
    mbw = surface_size.bit_length() - 1  # max bin width, num trailing zeros

    position = mbw  # special case the first one-bin segment
    mbw -= 1  # new largest bin width is one less than the first
    n -= 1  # we've handled one bin

    # get the next all-1s number less than or equal to n
    # subtract one from perfect square gets an all 1's number
    completed_bins = bit_floor(n + 1) - 1
    assert completed_bins.bit_length() == completed_bins.bit_count()
    assert n // 2 <= completed_bins <= n
    # assert lt == completed_bins
    ncs = completed_bins.bit_length()  # num completed segments

    # clever/tricky part...
    # one-shot sum of all bin widths segments that are completely full...
    # equivalent to iterative sum of bin segment sizes times bin width
    # where bin width segment size doubles each iteration and bin segment size
    # decreases by one each iteration

    # https://www.wolframalpha.com/input?i=%5Csum_%7Bj%3D0%7D%5E%7Bb-1%7D+q+%5Ccdot+2%5Ej
    position += (1 << ncs) * mbw - mbw
    # equiv: cum += sum(mbw << j for j in range(ncs))

    # https://www.wolframalpha.com/input?i=-2+%28-1+%2B+2%5En%29+%2B+2%5En+n&assumption=%22ClashPrefs%22+-%3E+%7B%22Math%22%7D
    position -= ncs * (1 << ncs) - (1 << (ncs + 1)) + 2
    # equiv: cum -=  sum(j << j for j in range(ncs))

    # ... and now handle the remaining partially-filled bin segment, if any
    num_unhandled_bins = n - completed_bins
    unhandled_segment_bin_width = mbw - ncs
    position += num_unhandled_bins * unhandled_segment_bin_width

    return position
