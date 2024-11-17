from ._bitlen32_scalar import bitlen32_scalar
from ._jit import jit


@jit(nopython=True)
def ctz_scalar(x: int) -> int:
    """Count trailing zeros."""
    return bitlen32_scalar(x & -x) - 1
