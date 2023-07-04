import itertools as it
import typing

from deprecated import deprecated

from .....pylib import bit_ceil


@deprecated(reason="Uses generator. Should refactor to functional form.")
def iter_hanoi_invader_values(hanoi_value: int) -> typing.Iterator[int]:
    """What hanoi values will deposit over sites that had last been reserved
    for `hanoi_value`?

    Note that this sequence is independent of `surface_size`.
    """
    for i in it.count():
        # (1 >> i) equiv 2**i
        yield hanoi_value + bit_ceil(hanoi_value + 1) * (1 << i)
