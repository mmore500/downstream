from .....pylib import hanoi
from .._impl import get_num_reservations_provided
from ._impl import (
    calc_rank_of_deposited_hanoi_value,
    get_reservation_index_elimination_rank,
    iter_candidate_hanoi_occupants,
    iter_candidate_reservation_indices,
)


def calc_resident_deposition_rank(
    site: int, surface_size: int, num_depositions: int
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """

    # special case for zero depositions,
    # which would correspond to a nonsensical negative rank
    if num_depositions == 0:
        return 0
    rank = num_depositions - 1

    # look back through time for the most recent hanoi value `site` has been
    # reserved for under which
    # 1. site would have fallen within its initial set of incidence reservation
    #    buffer positions (the naive number of buffer positions may have never
    #    been realized for "safety" alignment timing)
    # 2. there have actually been enough depositions of the candidate hanoi
    #    value to reach the site's semantic index within the incidence
    #    reservation buffer at least once
    # if at least one of these conditions is not fulfilled, then no deposition
    # associated with the candidate hanoi value would have ever taken place at
    # site
    # so, continue with the loop to check the preceding hanoi value that could
    # have deposited there (it would still be around because it would have
    # never been overwritten)
    candidate_zip = zip(
        iter_candidate_hanoi_occupants(site, rank),
        iter_candidate_reservation_indices(site, surface_size, rank),
    )
    for candidate_hanoi_value, candidate_reservation_index in candidate_zip:
        # deadline_rank: one past the last time that candidate hanoi value
        # could have possibly been deposited at site (because at this point
        # the incidence reservation buffer position associated with site for
        # the candidate hanoi value was dropped)
        deadline_rank = get_reservation_index_elimination_rank(
            candidate_hanoi_value,
            candidate_reservation_index,
            surface_size,
        )
        if deadline_rank is None:
            # None means that is candidate_reservation_index is out of bounds
            # for even the largest incidence reservation buffer sie associated
            # with candidate_hanoi_value (i.e., the buffer size at zeroth
            # incidence)
            # thus, candidate hanoi value could never have deposited at site
            # and we can skip this value

            # assert some assumptions related to using break instead of
            # continue below
            assert all(
                get_reservation_index_elimination_rank(
                    candidate_hanoi_value_,
                    candidate_reservation_index_,
                    surface_size,
                )
                is None
                and (
                    candidate_hanoi_value_ / candidate_reservation_index_
                    <= candidate_hanoi_value / candidate_reservation_index
                )
                for (
                    candidate_hanoi_value_,
                    candidate_reservation_index_,
                ) in candidate_zip
                if candidate_hanoi_value_ > 0
            ), {
                "candidate_hanoi_value": candidate_hanoi_value,
                "candidate_reservation_index": candidate_reservation_index,
                "max_num_reservations_provided": get_num_reservations_provided(
                    0, surface_size, 0
                ),
                "surface_size": surface_size,
                "rank": rank,
                "site": site,
            }
            # why can we break instead of just continuing? todo
            break  # continue also works here

        assert deadline_rank, {
            "candidate_hanoi_value": candidate_hanoi_value,
            "candidate_reservation_index": candidate_reservation_index,
            "rank": rank,
            "site": site,
            "surface_size": surface_size,
        }

        assert deadline_rank
        # focal rank: the very last possible time when a deposition of
        # candidate_hanoi_value could have been performed onto site
        # (at subsequent time points, that site is dropped from
        # candidate_hanoi_value's incidence reservation buffer)
        focal_rank = min(rank, deadline_rank - 1)
        assert focal_rank <= rank

        # how many depositions of candidate_hanoi_value have been performed
        # before the site is dropped from candidate_hanoi_value's incidence
        # reservation buffer?
        hanoi_count = hanoi.get_incidence_count_of_hanoi_value_through_index(
            candidate_hanoi_value,
            focal_rank,
        )
        # have enough depositions of candidate_hanoi_value value been performed
        # to fill up candidate_hanoi_value's incidence reservation buffer
        # sufficiently to reach site and put a value there?
        # if this is the case, then the resident deposition at site is
        # associated with candidate_hanoi_value
        # TODO: factor this process of determining the hanoi value resident at
        # site out into a support function
        if hanoi_count > candidate_reservation_index:
            # candidate_hanoi_value is the hanoi value associated with the
            # deposition resident at site
            # ... use this information to deduce the rank at which the resident
            # deposition at site was deposited
            res = calc_rank_of_deposited_hanoi_value(
                candidate_hanoi_value,
                candidate_reservation_index,
                surface_size,
                focal_rank,
            )
            assert res <= rank, {
                "candidate_hanoi_value": candidate_hanoi_value,
                "candidate_reservation_index": candidate_reservation_index,
                "deadline_rank": deadline_rank,
                "focal_rank": focal_rank,
                "hanoi_count": hanoi_count,
                "rank": rank,
                "res": res,
                "site": site,
                "surface_size": surface_size,
            }
            return res

        # candidate_hanoi_value did not have enough depositions to make it to
        # site, so whatever hanoi value site was allocated to beforehand would
        # still be the resident deposition (if it succeeded in reaching the
        # corresponding incidence reservation buffer position of site)
        # ... so, continue with loop to look at the next candidate

    # fall-through case: the site has not been deposited on, so the site holds
    # the randomly-generated differentia that the surface was initialized with
    return 0
