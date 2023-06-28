"""Will correspond to
`04-incrementing-incidence-reservation-surface-with-safety-aligned-transition.ipynb`."""

from ._calc_resident_deposition_rank import calc_resident_deposition_rank
from ._iter_resident_deposition_ranks import iter_resident_deposition_ranks
from ._pick_deposition_site import pick_deposition_site

__all__ = [
    "calc_resident_deposition_rank",
    "iter_resident_deposition_ranks",
    "pick_deposition_site",
]
