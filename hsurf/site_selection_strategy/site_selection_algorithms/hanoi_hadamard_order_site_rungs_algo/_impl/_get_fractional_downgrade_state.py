import typing

from deprecated.sphinx import deprecated

from .....pylib import fast_pow2_divide, hanoi
from ._get_num_incidence_reservations_at_rank import (
    get_num_incidence_reservations_at_rank,
)
from ._has_hanoi_value_filled_first_reservation_layer import (
    has_hanoi_value_filled_first_reservation_layer,
)
from ._iter_hanoi_invader_values import iter_hanoi_invader_values


@deprecated(
    reason="Needs extensive refactor: break into smaller pieces, "
    "unroll/remove attempt loop, avoid monolithic bundled return value, and "
    "rename to follow 'site rung' terminology.",
    version="0.0.0",
)
def get_fractional_downgrade_state(
    hanoi_value: int, surface_size: int, rank: int
) -> typing.Optional[typing.Dict]:
    """Dispatches fractional reservation buffer degradation (i.e., dropping
    incidence reservation ring buffer slots less than half at a time).

    Proceeds three parts:
    1. DETERMIINE ELIGIBILTY FOR FRACTIONAL DOWNGRADE,
    2. DETERMINE FRACTIONAL DOWNGRADE PROVIDED GRANULARITY, and
    3. DETERMINE CURRENT STAGE WITHIN FRACTIONAL DOWNGRADE PROCESS.

    ## Part I
    Determines whether fractional downgrade can be performed safely. If there
    is not enough time to traverse sufficient ring buffer positions to ensure
    safe alignment before the first invader deposit or between invader
    depositions, returns None. Note that safe alignment must not only position
    the most recently deposited value at the correct ring buffer slot but must
    also simultaneously align on a "virtual" clock face of the original buffer
    size to enable stateless bookkeeping.

    ## Part II
    Then, determines what granularity the duration between the ring buffer
    positions is capable of supporting. Granularity means the chunk size of
    incidence reservation ring buffer sites that is dropped at once. The
    minimal granularity is half of the eligible-for-invasion buffer (one
    quarter of the total ring buffer). Granularity can be subdivided into
    dyadic fractions (1/2, 1/4, etc.), down to one ring buffer site at a time.
    The smallest safe granularity is used. Granularity is constant for a
    particular fractionally-downgraded hanoi invasion.

    ## Part III
    Finally, calculates the stage of progress within the current fractional
    downgrade process. Note that the stage is expressed in terms of the current
    downgrade _transition_ in play instead of the number of incidence
    reservation ring buffer positions eliminated (termed the "subtrahend") at
    the current rank. The timing of transition between "current subtrahend" and
    "next subtrahend" (e.g., which side of the transition the current rank
    falls at) is controlled elsewhere, relying on `get_safe_downgrade_rank`.

    Note that if the final downgrade has been dispatched within the current
    invasion cycle, this function will plan for the first downgrade of the next
    invasion cycle during the period before the first deposit of the invader
    hanoi value.

    Returns
    -------
    None if the focal hanoi invasion cycle is ineligible for fractional
    downgrade. Otherwise, a dict detailing the parameters of the supported
    fractional downgrade and the current stage within the downgrade process.

    Notees
    ------
    Needs extensive housekeeping. Should be broken up. There are some
    redundancies that can be stripped away. Also a possibility for less
    restrictive determination of fractional downgrade eligiblity. See in-code
    comments.
    """
    # PART I: DETERMIINE ELIGIBILTY FOR FRACTIONAL DOWNGRADE
    # ======================================================
    # if ineligible for a fractional (site-runged) downgrade, external logic
    # will fall back to term-runged downgrade

    # get the first invading hanoi value that may (or may not) have started
    # ivading but hasn't yet wrapped up invading
    # (if it has completed invading, go to the next candidate invader value)
    for invading_hanoi_value in iter_hanoi_invader_values(hanoi_value):
        if not has_hanoi_value_filled_first_reservation_layer(
            invading_hanoi_value, surface_size, rank
        ):
            break

    assert invading_hanoi_value > hanoi_value

    # check for fractional downgrade eligibility
    # if current invasion cycle is ineligible for fractional downgrade, but the
    # current invasion has started (so the fallback downgrade would have
    # dispatched)
    for attempt in 1, 2:
        invader_cadence = hanoi.get_hanoi_value_index_cadence(
            invading_hanoi_value
        )
        # protagonist meaning the hanoi value whose incidence reservation ring
        # buffer we are deciding
        protagonist_cadence = hanoi.get_hanoi_value_index_cadence(hanoi_value)

        # if hanoi invader value is past halfway of buffer slots, there will
        # only be two total incidence reservation ring buffer slots and only
        # one "to-be-  dropped" during current invasion...
        # fractional degradation is meaningless, mark ineligible for fractional
        # degradation to fall back to simpler "drop half at a time" impl
        # possibly redundant with check below
        if invading_hanoi_value > fast_pow2_divide(surface_size, 2):
            return None

        # first incidence of invading hanoi value
        invasion_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
            invading_hanoi_value, 0
        )
        num_reservations = get_num_incidence_reservations_at_rank(
            invasion_rank, surface_size
        )

        # if there is only one to-be-dropped-in-invasion incidence reservation
        # ring buffer slot (i.e., two total slots), fractional degradation is
        # meaningless...
        # fall back to simpler "drop half at a time" impl to drop single slot
        # possibly redundant with check above
        if num_reservations == 1:
            return None

        # tour meaning the number of sites in the full ring buffer
        tour_size = 2 * num_reservations

        # how many ranks to make a complete circuit through the ring buffer?
        protagonist_tour_time = tour_size * protagonist_cadence
        num_protagonist_cycles_per_invader_cadence = fast_pow2_divide(
            invader_cadence, protagonist_tour_time
        )
        if num_protagonist_cycles_per_invader_cadence >= (
            # see test_calc_dyadic_lcm_upper_bound.py
            # https://github.com/mmore500/hstrat-surface-concept/blob/4d0eca2ae3fe1890983889fdb8a8482fd3b24627/pylib/test/test_calc_dyadic_lcm_upper_bound.py#L39
            4
            * tour_size
        ):
            # success!
            # we have enough time between invader depositions to perform
            # safe alignment at *some* granularity (i.e., at least 1/2 of "to-
            # be-dropped" slots from current invasion)
            break

        if attempt == 1 and invasion_rank <= rank:
            # current invasion cycle isn't eligible for fractional downgrade
            # but the invasion is already underway so the non-fractional,
            # half-of-reservations downgrade has been dispatched...
            # look forward to the next invasion; try again with the next
            # invading hanoi value and if that invasion is eligible for
            # fractional downgrade then proceed (in the rest of the body) to
            # plan for that downgrade cycle
            invading_hanoi_value = (
                hanoi_value + (invading_hanoi_value - hanoi_value) * 2
            )
        else:
            pass
            # it's janky that this does a second redundant attempt under this
            # case: needs cleanup
    else:
        # if for loop does not reach break condition, report ineligible for
        # fractional deposition
        return None

    # PART II: DETERMINE FRACTIONAL DOWNGRADE PROVIDED GRANULARITY
    # ============================================================
    # see test_calc_dyadic_lcm_upper_bound.py
    # https://github.com/mmore500/hstrat-surface-concept/blob/4d0eca2ae3fe1890983889fdb8a8482fd3b24627/pylib/test/test_calc_dyadic_lcm_upper_bound.py#L39
    # num_granules * tour_size * 2 == num_protagonist_cycles_per_invader_cadence
    # num_granules == num_protagonist_cycles_per_invader_cadence // (tour_size * 2)
    num_granules = min(
        fast_pow2_divide(
            num_protagonist_cycles_per_invader_cadence, (tour_size * 2)
        ),
        num_reservations,
    )
    assert 1 < num_granules <= num_reservations
    granule_size = fast_pow2_divide(num_reservations, num_granules)
    assert granule_size

    # PART III: DETERMINE CURRENT STAGE WITHIN FRACTIONAL DOWNGRADE PROCESS
    # ========================================================================

    # GLOSSARY
    # --------
    # subrahend: number of incidence reservation ring buffer positions that
    # should be subtracted away from originally-available buffer size to get
    # the current number of "provided" buffer positions; put another way, the
    # number of dropped buffer slots during current hanoi invasion.
    # Will range from zero to half of available buffer positions
    #
    # current/next subtrahend: the ring buffer downsize (slot drop) transition
    # currently being managed. The exact rank to perform the transition at is
    # determined elsewhere (chosen to ensure "safe" transition rank when
    # oldest buffer values will be dropped). Note that the "next" subtrahend
    # will be "currently" be in use after that transition rank has been
    # reached. (It may mke more sense to name these "from" and "to.")
    #
    # raw/granularized subtrahend: in some cases, if incidence reservation
    # buffer slots were dropped one-by-one there would not be sufficient time
    # to reach "safe" downgrade positions between invader hanoi value
    # depositions. We can reach "safe" downgrade positions more frequenty by
    # dropping chunks of slots sized as a dyadic fraction (1/2, 1/4, 1/8, etc.)
    # of eligible-to-drop (i.e., being-invaded) slots. (Note that the number of
    # eligible-to-drop is a power of 2.) (Safe downgrade positions are reached
    # more frequenly because these synchronize to the "virtual" original buffer
    # size clock face [required to enable stateless bookkeeping] more often.)

    # raw means before taking granularity into account
    # what subtrahend would be
    raw_current_subtrahend = (
        hanoi.get_incidence_count_of_hanoi_value_through_index(
            invading_hanoi_value,
            rank,
        )
    )
    raw_next_subtrahend = raw_current_subtrahend + 1
    assert raw_next_subtrahend > raw_current_subtrahend

    # granule is measured in "raw" slot counts contained within a chunk
    current_subtrahend_granule = fast_pow2_divide(
        # adding granule size - 1 rounds up
        raw_current_subtrahend + granule_size - 1,
        granule_size,
    )
    assert current_subtrahend_granule <= raw_current_subtrahend
    assert bool(current_subtrahend_granule) == bool(raw_current_subtrahend)

    next_subtrahend_granule = fast_pow2_divide(
        # adding granule size - 1 rounds up
        raw_next_subtrahend + granule_size - 1,
        granule_size,
    )
    assert next_subtrahend_granule <= raw_next_subtrahend
    assert bool(next_subtrahend_granule) == bool(raw_next_subtrahend)

    # granularized subtrahend measured in "raw" slot count,
    # will be an even multiple of chunk size
    granularized_current_subtrahend = current_subtrahend_granule * granule_size
    assert granularized_current_subtrahend >= raw_current_subtrahend

    # note that granularized current and next subtrahend can be equal
    # this works (downgrade step is a nop) but there might be a better paradigm
    # that could be refactored to
    # (in fact, this might enable more efficient granularization by taking into
    # account that granularization increases the time between invasions that
    # must be aligned at)
    granularized_next_subtrahend = next_subtrahend_granule * granule_size
    assert granularized_next_subtrahend >= raw_next_subtrahend

    # note: negative downgrade rank not allowed
    # we should have delegated to the simpler term-runged implementation
    # (which may end up requesting a negative downgrade rank itself)
    assert (
        0
        <= granularized_current_subtrahend
        <= granularized_next_subtrahend
        <= num_reservations
    )

    upcoming_invader_rank = hanoi.get_index_of_hanoi_value_next_incidence(
        invading_hanoi_value, rank
    )
    # just a sanity check...
    # upcoming invader rank should always be greater than current rank
    assert upcoming_invader_rank > rank

    # monolithic package of entire fractional downgrade ,
    # including some unnecessary information for safety checks (i.e., asserts)
    # and debugging
    # (this should be refactored away)
    return {
        "hanoi value": hanoi_value,
        "hanoi cadence": protagonist_cadence,
        "upcoming invader rank": upcoming_invader_rank,
        "first invasion rank": invasion_rank,
        "invader cadence": invader_cadence,
        "invading hanoi value": invading_hanoi_value,
        "current subtrahend": granularized_current_subtrahend,
        "next subtrahend": granularized_next_subtrahend,
        "tour size": tour_size,
        "num granules": num_granules,
        "granule size": granule_size,
    }
