"""Transplanted from
`05-fractional-incrementing-incidence-reservation-surface-with-safety-aligned-transition.ipynb`"""

from ._iter_resident_ranks import iter_resident_ranks
from ._resolve_rank_at_site import resolve_rank_at_site
from ._select_deposit_site import select_deposit_site

__all__ = [
    "iter_resident_ranks",
    "resolve_rank_at_site",
    "select_deposit_site",
]
