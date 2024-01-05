"""Transplanted from
`05-fractional-incrementing-incidence-reservation-surface-with-safety-aligned-transition.ipynb`"""

from ._enact import pick_deposition_site
from ._scry import (
    calc_resident_deposition_rank,
    iter_resident_deposition_ranks,
)

__all__ = [
    "calc_resident_deposition_rank",
    "iter_resident_deposition_ranks",
    "pick_deposition_site",
]
