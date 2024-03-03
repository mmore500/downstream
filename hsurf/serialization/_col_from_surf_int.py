import types
import typing

from hstrat import hstrat
from hstrat._auxiliary_lib import bit_drop_msb
from hstrat.serialization._impl._DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH import (
    DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH,
)

from ._col_from_surf_packet import col_from_surf_packet


def col_from_surf_int(
    value: int,
    differentia_bit_width: int,
    site_selection_algo: types.ModuleType,
    differentiae_byte_bit_order: typing.Literal["big", "little"] = "big",
    num_strata_deposited_byte_order: typing.Literal["big", "little"] = "big",
    num_strata_deposited_byte_width: int = (
        DEFAULT_PACKET_NUM_STRATA_DEPOSITED_BYTE_WIDTH
    ),
    value_byte_width: typing.Optional[int] = None,
) -> hstrat.HereditaryStratigraphicColumn:
    """Deserialize a `HereditaryStratigraphicColumn` from an integer
    representation of packed hsurf data.

    Packet should contain (1) a stratum deposition count followed by (2)
    binary-packed differentia values. Each component must align evenly with
    byte boundaries.

    Integer representation is packet binary representation plus a sentry bit
    at the most significant bit position. Sentry bit prevents loss of leading
    zero bits. If `value_byte_width` is not `None`, an appropriate sentry bit
    is added to the value if it is not already present.

    Assumes big endian byte order.
    """

    if value_byte_width is not None:
        assert value.bit_length() <= value_byte_width * 8
        value |= 1 << (value_byte_width * 8)  # sentry bit

    if value.bit_length() % 8 != 1:  # sentry bit
        raise ValueError(
            f"Invalid integer representation {value} {bin(value)}. "
            "Must be an even byte multiple plus sentry bit. "
            "Probably missing sentry bit.",
        )
    semantic_value = bit_drop_msb(value)  # drop sentry bit
    buffer = semantic_value.to_bytes(
        (value.bit_length() - 1) // 8, byteorder="big", signed=False
    )
    return col_from_surf_packet(
        packet=buffer,
        differentia_bit_width=differentia_bit_width,
        site_selection_algo=site_selection_algo,
        differentiae_byte_bit_order=differentiae_byte_bit_order,
        num_strata_deposited_byte_order=num_strata_deposited_byte_order,
        num_strata_deposited_byte_width=num_strata_deposited_byte_width,
    )
