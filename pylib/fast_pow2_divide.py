def fast_pow2_divide(dividend, divisor):
    assert dividend >= 0
    assert divisor >= 1
    assert divisor.bit_count() == 1

    # Count the number of trailing zeros, which is equivalent to log2(divisor)
    shift_amount = (divisor - 1).bit_count()

    # Perform fast division using right shift
    return dividend >> shift_amount
