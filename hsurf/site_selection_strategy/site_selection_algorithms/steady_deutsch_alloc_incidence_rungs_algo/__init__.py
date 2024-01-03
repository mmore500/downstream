"""A steady time stratum deposition algorithm.

Categorizes ranks by hanoi values. Divides the surface into bins and waterfalls
successive instances of each hanoi values into each bin from left to right.
Positions within bins rotate in a cycle according to hanoi values.

Bins are arranged into same-capacity segments, with bin size decreasing from
left to right. Bin size decreases by one between each segment. The first two bin
segments have one bin each. The next has two bins, then four, then eight, etc.
The last segment occupies one fourth of the surface with size-one bins.

The rationale behind bin shrink is that at any given time, the number of hanoi
values `v` that have been observed will be twice the number of hanoi values
`v + 1` that have been observed. So, we need bigger bins to hold larger
collections of hanoi values earlier on. This distributional pattern is
self-similar/scale invariant, so the bin distribution is useful indefinitely.

The specific bin distribution used is based on how the initial fill of a surface
fills with hanoi values.

This algorithm could be optimized by looping hanoi values back over for a second
pass on sites that haven't been filled yet once the end of the waterfall is
reached. That bookkeeping is not implemented in this version.
"""


from ._enact._pick_deposition_site import pick_deposition_site
from ._scry._calc_resident_deposition_rank import calc_resident_deposition_rank
from ._scry._iter_resident_deposition_ranks import (
    iter_resident_deposition_ranks,
)

__all__ = [
    "calc_resident_deposition_rank",
    "iter_resident_deposition_ranks",
    "pick_deposition_site",
]
