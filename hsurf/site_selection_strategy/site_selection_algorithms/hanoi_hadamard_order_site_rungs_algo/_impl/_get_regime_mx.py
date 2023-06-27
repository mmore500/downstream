from deprecated.sphinx import deprecated

from ._is_hanoi_invadable_and_uninvaded import is_hanoi_invadable_and_uninvaded


# redundant with is_2x_reservation_eligible?
@deprecated(
    reason="Should rename 'regime.'",
    version="0.0.0",
)
def get_regime_mx(hanoi_value: int, rank: int) -> int:
    """Implemenentation detail.

    Used in non-fractional reservation incrementing mode (when fractional
    incrementing is not eligible). Controls halving of reservation upon hanoi
    invasion.
    """
    if is_hanoi_invadable_and_uninvaded(hanoi_value, rank):
        return 2
    else:
        return 1
