import types
import typing

from hstrat import hstrat
from hstrat.serialization._impl._DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH import (
    DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH,
)
import typing_extensions

from ..interop import make_stratum_retention_policy_from_site_selection_algo
from ._sort_differentiae_by_deposition_rank import (
    sort_differentiae_by_deposition_rank,
)


def col_from_surf_packet(
    packet: typing_extensions.Buffer,
    differentia_bit_width: int,
    site_selection_algo: types.ModuleType,
    differentiae_byte_bit_order: typing.Literal["big", "little"] = "big",
    num_strata_deposited_byte_order: typing.Literal["big", "little"] = "big",
    num_strata_deposited_byte_width: int = (
        DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH
    ),
) -> hstrat.HereditaryStratigraphicColumn:
    """Deserialize downstream data into a `HereditaryStratigraphicColumn` from a
    differentia packet and column configuration specification information.

    Packet should contain (1) a stratum deposition count followed by (2)
    binary-packed differentia values. Each component must align evenly with
    byte boundaries.
    """

    num_strata_deposited = int.from_bytes(
        packet[:num_strata_deposited_byte_width],
        byteorder=num_strata_deposited_byte_order,
        signed=False,
    )
    num_differentia_bytes = len(packet) - num_strata_deposited_byte_width
    num_differentia_bits = num_differentia_bytes * 8
    if num_differentia_bits % differentia_bit_width != 0:
        raise NotImplementedError
    surface_size = num_differentia_bits // differentia_bit_width
    surface_differentia_values = hstrat.unpack_differentiae_bytes(
        packet[num_strata_deposited_byte_width:],
        differentia_bit_width=differentia_bit_width,
        differentiae_byte_bit_order=differentiae_byte_bit_order,
        num_packed_differentia=surface_size,
    )
    column_differentia_values = sort_differentiae_by_deposition_rank(
        differentiae=surface_differentia_values,
        num_strata_deposited=num_strata_deposited,
        site_selection_algo=site_selection_algo,
    )
    column_strata = [
        hstrat.HereditaryStratum(
            differentia=value,
            differentia_bit_width=differentia_bit_width,
        )
        for value in column_differentia_values
    ]

    store = hstrat.HereditaryStratumOrderedStoreList()
    ranks = sorted(
        set(
            site_selection_algo.iter_resident_deposition_ranks(
                surface_size,
                num_strata_deposited,
            ),
        ),
    )
    for rank, stratum in zip(ranks, column_strata):
        store.DepositStratum(rank=rank, stratum=stratum)

    stratum_retention_policy = (
        make_stratum_retention_policy_from_site_selection_algo(
            site_selection_algo,
        )(surface_size)
    )
    assert stratum_retention_policy.CalcNumStrataRetainedExact(
        num_strata_deposited,
    ) == len(column_strata)

    return hstrat.HereditaryStratigraphicColumn(
        stratum_retention_policy=stratum_retention_policy,
        stratum_differentia_bit_width=differentia_bit_width,
        stratum_ordered_store=(store, num_strata_deposited),
        always_store_rank_in_stratum=False,
    )
