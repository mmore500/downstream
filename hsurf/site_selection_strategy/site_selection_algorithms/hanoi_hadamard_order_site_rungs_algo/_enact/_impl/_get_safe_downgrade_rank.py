from deprecated.sphinx import deprecated

from ...... import pylib


@deprecated(
    reason="Need to revise function signature to remove debugging cruft.",
    version="0.0.0",
)
def get_safe_downgrade_rank(
    cycle_num_ranks: int,
    required_cycle_rank_position: int,
    required_lag: int,
    end_rank: int,
    hanoi_offset: int,
    cadence_for_asserts: int,  # debugging parameter
    hanoi_value_for_asserts: int,  # debugging parameter
) -> int:
    """Handles math for modulus alignments to ensure safe downgrades (i.e.,
    the oldest values are dropped last from the incidence reservation ring
    buffer and not out of the middle of the newer values).

    Parameters
    ----------
    cycle_num_ranks : int
        The modulus (size of the modular arithmetic "clock face"), measured as
        the number of deposition ranks required to make a full trip around the
        reservation instance ring buffer.
    required_cycle_rank_position : int
        At which absolute position on the clock face do we need to stop? Measured as deposition ranks relative to alignment at the zeroth
        incidence reservation.
    required_lag : int
        How long before the deadline do we need to stop, at minimum? Time unit
        is in deposition ranks.
    end_rank : int
        What is the deadline we must stop before? Time unit is in deposition
        ranks. In practice, this will be related to (equal to?) the time that
        the available reservation slots is invaded by high hanoi values from
        the spatially-preceding reservation slot.
    hanoi_offset : int
        At what rank does the incidence of the focal hanoi value occur?

    Returns
    -------
    int
        The deposition rank satisfying parameter criteria, e.g., when the
        incidence reservation ring buffer size can be safely reduced.

    Notes
    -----
    The distribution of occurence the focal hanoi value over the hanoi sequence
    moderates the relationship between clock face ring buffer position and
    ranks. Each occurence of the focal hanoi value advances the ring buffer one
    position around the clock face. The first deposition aligns with position
    zero on the clock face. Each hanoi value occurs after a known rank offset,
    and then occurs at a steady rank tempo (which is larger than the offset).

    Used in both fractional and non-fractional reservation degradation modes.
    """

    offset = hanoi_offset
    hanoi_value = hanoi_value_for_asserts

    assert cadence_for_asserts
    cadence = cadence_for_asserts

    assert cycle_num_ranks
    assert required_cycle_rank_position < cycle_num_ranks
    assert required_lag % cadence == 0
    # oc is offset corrected
    end_rank_oc = end_rank - offset

    deadline_rank_oc = end_rank_oc - required_lag
    #
    #    tt_below |             | goal
    #########################################################
    #             |----tour time----|
    #             |             :   |
    #                                           ^ end_rank
    #                              ^deadline rank
    #               ^mapped to here (intermediate)
    #             ^ then to here
    #                            ^ then to here
    #
    #########################################################
    #             |----tour time----|
    #             |             :   |          :  |
    #                                                    ^ end_rank
    #                                         ^deadline rank
    #                              ^mapped to here (intermediate)
    #             ^ then to here
    #                           ^ then to here
    #
    intermediate_oc = deadline_rank_oc - required_cycle_rank_position
    assert deadline_rank_oc - intermediate_oc <= cycle_num_ranks

    tt_below_oc = intermediate_oc - pylib.modulo(
        intermediate_oc, cycle_num_ranks
    )
    assert tt_below_oc % cadence == 0
    assert tt_below_oc % cycle_num_ranks == 0
    assert (
        deadline_rank_oc - tt_below_oc
        <= cycle_num_ranks + required_cycle_rank_position
    )

    goal_oc = tt_below_oc + required_cycle_rank_position
    assert goal_oc % cycle_num_ranks == required_cycle_rank_position
    assert goal_oc % cadence == 0
    assert goal_oc <= deadline_rank_oc
    assert goal_oc - deadline_rank_oc <= cycle_num_ranks

    downgrade_rank = goal_oc + offset
    assert downgrade_rank <= end_rank
    assert (
        required_lag
        <= end_rank - downgrade_rank
        <= cycle_num_ranks + required_lag
    )

    assert cycle_num_ranks % cadence == 0
    assert (
        pylib.hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, offset
        )
    ) % cycle_num_ranks == 1
    assert (
        pylib.hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, offset + cadence
        )
    ) % cycle_num_ranks == 2

    assert cycle_num_ranks % cadence == 0
    if tt_below_oc + offset >= 0:
        assert tt_below_oc % cadence == 0
        assert tt_below_oc % cycle_num_ranks == 0
        assert (
            pylib.hanoi.get_incidence_count_of_hanoi_value_through_index(
                hanoi_value, tt_below_oc + offset
            )
            - 1
        ) % (cycle_num_ranks // cadence) == 0
    if downgrade_rank >= 0:
        assert (downgrade_rank + cadence - offset) % cadence == 0
        assert (
            pylib.hanoi.get_incidence_count_of_hanoi_value_through_index(
                hanoi_value, downgrade_rank
            )
            - 1
        ) % (cycle_num_ranks // cadence) == (
            required_cycle_rank_position // cadence
        )

    return downgrade_rank
