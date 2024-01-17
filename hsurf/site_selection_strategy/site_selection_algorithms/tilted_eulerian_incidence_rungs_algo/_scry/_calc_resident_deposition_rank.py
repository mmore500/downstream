from .....pylib import hanoi, fast_pow2_mod
from .._enact._pick_deposition_site import pick_deposition_site
from .._impl import (
    calc_invading_hanoi_value,
    calc_hanoi_invasion_rank,
    calc_resident_hanoi_value,
    get_epoch_rank,
    get_global_epoch,
    get_global_num_reservations,
    get_hanoi_num_reservations,
    get_reservation_position_physical,
    get_site_hanoi_value_assigned,
    get_site_reservation_index_logical,
)


def _finalize(
    hanoi_value,
    reservation,
    num_reservations,
    rank,
):
    assert reservation < num_reservations

    incidence_seen = (
        hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, rank
        )
        - 1
    )
    assert incidence_seen >= 0

    if incidence_seen < reservation:
        return 0

    site_incidence = (
        incidence_seen
        - fast_pow2_mod(incidence_seen, num_reservations)
        + reservation
    )
    if site_incidence > incidence_seen:
        site_incidence -= num_reservations
    assert 0 <= site_incidence
    assert site_incidence <= incidence_seen
    res = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value, site_incidence
    )

    return res


def _get_epoch_rank(hanoi_value, rank, surface_size):
    epoch = get_global_epoch(rank, surface_size)
    epoch_rank = get_epoch_rank(epoch, surface_size)
    assert epoch_rank <= rank

    if epoch:
        invasion_rank = calc_hanoi_invasion_rank(
            hanoi_value, epoch, surface_size
        )
        if invasion_rank <= rank:
            epoch_rank = invasion_rank
    return epoch_rank


def _get_cur_epoch_hanoi_count(hanoi_value, rank, surface_size):
    epoch_rank = _get_epoch_rank(hanoi_value, rank, surface_size)
    res = hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, rank
    ) - hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, epoch_rank
    )
    assert res >= 0
    return res


def calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
    _recursion_depth: int = 0,
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """
    # print()
    assert _recursion_depth < 2
    if num_depositions == 0:
        return 0

    rank = num_depositions - 1

    actual_hanoi_value = calc_resident_hanoi_value(
        site, surface_size, num_depositions
    )
    assigned_hanoi_value = get_site_hanoi_value_assigned(
        site, rank, surface_size
    )

    if actual_hanoi_value == assigned_hanoi_value:
        reservation = get_site_reservation_index_logical(
            site, rank, surface_size
        )
        num_reservations = get_hanoi_num_reservations(
            rank, surface_size, actual_hanoi_value
        )
        assert reservation < num_reservations
        # assert num_reservations == get_hanoi_num_reservations(
        #     rank, surface_size, hanoi_value=actual_hanoi_value
        # )
        res = _finalize(actual_hanoi_value, reservation, num_reservations, rank)
        assert res < num_depositions

        cehc = _get_cur_epoch_hanoi_count(
            actual_hanoi_value, rank, surface_size
        )
        if cehc > reservation:
            return res
        else:
            prev_epoch_rank = (
                _get_epoch_rank(actual_hanoi_value, rank, surface_size) - 1
            )
            if prev_epoch_rank >= 0:
                num_reservations = get_hanoi_num_reservations(
                    prev_epoch_rank, surface_size, actual_hanoi_value
                )
                return _finalize(
                    actual_hanoi_value, reservation, num_reservations, rank
                )
            else:
                return res
            # while rank and pick_deposition_site(rank, surface_size) != site:
            #     rank -= 1
            # return rank
            # pass
            # epoch = get_global_epoch(rank, surface_size)
            # assert epoch
            # epoch_rank = get_epoch_rank(epoch, surface_size)
            # assert 0 < epoch_rank <= rank
            # return calc_resident_deposition_rank(
            #     site,
            #     surface_size,
            #     epoch_rank,  # +1/-1 cancel
            #     _recursion_depth + 1,
            # )

    elif actual_hanoi_value == 0 and rank < surface_size - 1:
        return 0

    while rank and pick_deposition_site(rank, surface_size) != site:
        rank -= 1

    return rank


#     if num_depositions == 0:
#         return 0

#     rank = num_depositions - 1
#     epoch = get_global_epoch(rank, surface_size)
#     epoch_rank = get_epoch_rank(epoch, surface_size)
#     if epoch_rank:
#         prev_epoch_rank = epoch_rank - 1
#         assert get_global_epoch(prev_epoch_rank, surface_size) == epoch - 1
#     else:
#         prev_epoch_rank = None

#     assigned_hanoi_value = get_site_hanoi_value_assigned(
#         site, rank, surface_size
#     )

#     num_reservations_g = get_global_num_reservations(rank, surface_size)
#     num_reservations_h = get_hanoi_num_reservations(
#         rank, surface_size, hanoi_value=actual_hanoi_value
#     )
#     has_been_invaded = num_reservations_g == num_reservations_h
#     num_reservations = num_reservations_h
#     if not has_been_invaded:
#         assert num_reservations_h == num_reservations_g * 2
#         assert prev_epoch_rank is not None
#         reservation = get_site_reservation_index_logical(
#             site, prev_epoch_rank, surface_size
#         )
#     else:
#         reservation = get_site_reservation_index_logical(
#             site, rank, surface_size
#         )

#     num_seen = hanoi.get_incidence_count_of_hanoi_value_through_index(
#         actual_hanoi_value, rank
#     )
#     epoch_incidence_count = (
#         hanoi.get_incidence_count_of_hanoi_value_through_index(
#             actual_hanoi_value, prev_epoch_rank
#         )
#         if epoch_rank  # special-case zeroth epoch
#         else 0
#     )
#     num_seen_this_epoch = num_seen - epoch_incidence_count
#     epoch_offset = fast_pow2_mod(epoch_incidence_count, num_reservations)

#     assert num_seen_this_epoch >= 0
#     if assigned_hanoi_value != actual_hanoi_value:
#         if rank < surface_size - 1:
#             return 0

#         # assert has_been_invaded
#         print("awooga", assigned_hanoi_value, actual_hanoi_value)
#         # go back one epoch
#         # assert assigned_hanoi_value < actual_hanoi_value
#         # num_reservations <<= 1  # double the number of reservations
#         # assert num_reservations >= 2
#         assert epoch > 0
#         assert epoch_rank > 0
#         # TODO don't go all the way back to prev epoch
#         invasion_rank = calc_hanoi_invasion_rank(
#             actual_hanoi_value, epoch, surface_size
#         )
#         assert invasion_rank <= rank, (rank, invasion_rank)

#         return calc_resident_deposition_rank(
#             site,
#             surface_size,
#             # +1 to translate to deposition count cancels with - 1
#             invasion_rank,
#             _recursion_depth + 1,
#         )
#         # reservation = get_site_reservation_index_logical(
#         #     site, prev_epoch_rank, surface_size
#         # )
#         # incidence = (
#         #     hanoi.get_incidence_count_of_hanoi_value_through_index(
#         #         actual_hanoi_value, prev_epoch_rank
#         #     )
#         #     - 1
#         # )
#         # assert incidence > 0
#         # assert 0 <= reservation < num_reservations, (
#         #     reservation,
#         #     num_reservations,
#         #     site,
#         #     rank,
#         #     actual_hanoi_value,
#         #     assigned_hanoi_value,
#         # )
#     elif reservation >= num_seen:
#         # handle case where the actual hanoi value has not yet been deposited
#         # this only occurs for hanoi value zero due to actual_hanoi_value
#         # being zero for undeposited sites
#         assert actual_hanoi_value == 0
#         print("bring", _recursion_depth, reservation, num_seen, rank)
#         return 0
#     elif (
#         num_seen_this_epoch <= reservation
#         and num_reservations_g == num_reservations_h
#     ):
#         print("broom")
#         num_reservations <<= 1  # double the number of reservations
#         assert num_reservations >= 2

#     assert num_seen
#     incidence_seen = num_seen - 1

#     if reservation > incidence_seen:
#         print("bing")
#         return 0

#     base_incidence = incidence_seen - fast_pow2_mod(
#         incidence_seen, num_reservations
#     )
#     cur_incidence_reservation = incidence_seen - base_incidence
#     assert 0 <= cur_incidence_reservation < num_reservations

#     site_incidence = (
#         base_incidence
#         + reservation
#         - num_reservations * (cur_incidence_reservation < reservation)
#     )
#     assert 0 <= site_incidence <= incidence_seen
#     res = hanoi.get_index_of_hanoi_value_nth_incidence(
#         actual_hanoi_value,
#         site_incidence,
#     )
#     assert 0 <= res <= rank
#     print(
#         f"""{_recursion_depth=}
# {assigned_hanoi_value=}
# {actual_hanoi_value=}
# {num_seen_this_epoch=}
# {incidence_seen=}
# {site_incidence=}
# {base_incidence=}
# {cur_incidence_reservation=}
# {reservation=}
# {num_reservations=}
# {surface_size=}
# {site=}
# {rank=}
# {res=}
# {epoch=}
# """,
#     )
#     return res

#     # reservation = get_site_reservation_index_logical(
#     #     site,
#     #     rank,
#     #     surface_size,
#     # )
#     # ansatz_hanoi = get_site_hanoi_value_assigned(
#     #     site,
#     #     rank,
#     #     surface_size,
#     # )

#     # if reservation >= num_seen and epoch == 0:
#     #     print(
#     #         f"c {num_seen=} {reservation=} {site=} {rank=} {surface_size=} {ansatz_hanoi=} {site=}"
#     #     )
#     #     return 0
#     # elif reservation >= num_seen:
#     #     assert epoch_rank > 0
#     #     print(
#     #         f"b {reservation=}, {num_seen=}, {rank=}, {ansatz_hanoi=} {site=}"
#     #     )
#     #     return calc_resident_deposition_rank(site, surface_size, epoch_rank)

#     # epoch_incidence_count = (
#     #     hanoi.get_incidence_count_of_hanoi_value_through_index(
#     #         ansatz_hanoi,
#     #         epoch_rank - 1,
#     #     )
#     #     if epoch_rank
#     #     else 0
#     # )
#     # num_seen_this_epoch = num_seen - epoch_incidence_count
#     # epoch_offset = fast_pow2_mod(epoch_incidence_count, num_reservations)

#     # assert num_seen_this_epoch >= 0
#     # # at_threshold = (rank + 1).bit_count() == 1
#     # if reservation >= num_seen_this_epoch:
#     #     assert epoch_rank > 0
#     #     print(
#     #         "a",
#     #         f"{reservation=}, {num_seen=}, {num_seen_this_epoch=}, {rank=} {epoch=} {ansatz_hanoi=} {site=}",
#     #     )
#     #     return calc_resident_deposition_rank(site, surface_size, epoch_rank)

#     # incidence_seen = num_seen - 1

#     # # max_genesis_hanoi = get_reservation_position_physical(1, surface_size) - 1
#     # # assert max_genesis_hanoi >= 0

#     # # else:
#     # #     assert num_seen > 0

#     # #     print(gnr)
