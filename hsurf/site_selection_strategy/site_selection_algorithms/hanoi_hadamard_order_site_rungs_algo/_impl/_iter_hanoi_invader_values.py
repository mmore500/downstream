import itertools as it
import typing

from deprecated import deprecated

from .....pylib import bit_ceil


@deprecated(reason="Uses generator. Should refactor to functional form.")
def iter_hanoi_invader_values(hanoi_value: int) -> typing.Iterator[int]:
    for i in it.count():
        yield hanoi_value + bit_ceil(hanoi_value + 1) * 2**i
