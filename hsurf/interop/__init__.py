from ._make_stratum_retention_algo_from_site_selection_algo import (
    make_stratum_retention_algo_from_site_selection_algo,
)

from ..site_selection_strategy.site_selection_algorithms import (
    steady_algo,
    tilted_algo,
    tilted_sticky_algo,
)

stratum_retention_interop_steady_algo = (
    make_stratum_retention_algo_from_site_selection_algo(steady_algo)
)
stratum_retention_interop_tilted_algo = (
    make_stratum_retention_algo_from_site_selection_algo(tilted_algo)
)
stratum_retention_interop_tilted_sticky_algo = (
    make_stratum_retention_algo_from_site_selection_algo(tilted_sticky_algo)
)


__all__ = [
    "make_stratum_retention_algo_from_site_selection_algo",
    "stratum_retention_interop_steady_algo",
    "stratum_retention_interop_tilted_algo",
    "stratum_retention_interop_tilted_sticky_algo",
]

# prevent names from leaking
del steady_algo
del tilted_algo
del tilted_sticky_algo
