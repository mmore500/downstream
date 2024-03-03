import types
import typing

import numpy as np


def sort_differentiae_by_deposition_rank(
    differentiae: typing.Iterable[int],
    num_strata_deposited: int,
    site_selection_algo: types.ModuleType,
) -> typing.List[int]:
    """Sort a collection of differentiae in chronological deposition order.

    This function takes an iterable of differentiae (integers), the number of
    strata that have been deposited, and a module that contains the site
    selection algorithm.

    It returns a list of differentiae sorted by their deposition ranks. If
    multiple founding differentiae (rank 0) are present, only one founding
    differentia will be returned (the longest-lasting founder).

    Parameters
    ----------
    differentiae : typing.Iterable[int]
        Differentiae in order of appearance on a hstrat surface.
    num_strata_deposited : int
        The number of strata that have been deposited onto the surface.
    site_selection_algo : types.ModuleType
        Site selection algorithm.

        Must provide `iter_resident_deposition_ranks`, that yields deposition
        ranks for the given surface size and number of strata deposited.

    Returns
    -------
    typing.List[int]
        A list of differentiae sorted by their deposition ranks, with one
        founding differentia (if any) at the beginning.
    """

    differentiae = [*differentiae]
    surface_size = len(differentiae)
    deposition_ranks = [
        *site_selection_algo.iter_resident_deposition_ranks(
            surface_size, num_strata_deposited
        ),
    ]

    argsort = np.argsort(deposition_ranks, kind="stable")
    sorted_by_rank = [*map(differentiae.__getitem__, argsort)]

    num_founding_sites = deposition_ranks.count(0)
    founder_elimination_order = [
        *site_selection_algo.iter_resident_deposition_ranks(
            surface_size, surface_size
        ),
    ]
    # simplifying assumption about the site selection algorithm
    assert set(founder_elimination_order) == set(range(surface_size))

    longest_founder = founder_elimination_order.index(0)
    # simplifying assumption about the site selection algorithm
    assert longest_founder == 0

    # take at most one founding differentia, the longest-lasting one
    founding_differentiae = sorted_by_rank[:num_founding_sites]
    nonfounding_differentiae = sorted_by_rank[num_founding_sites:]
    return [
        *founding_differentiae[:1],
        *nonfounding_differentiae,
    ]
