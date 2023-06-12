def modulo(a: int, b: int) -> int:
    """
    Calculate the mathematical modulo of 'a' with respect to 'b', ensuring a
    non-negative result.

    This function computes the modulo operation based on the mathematical
    definition, using the formula: (a % b + b) % b. This ensures that the
    result is non-negative even if 'a' is negative.

    Parameters
    ----------
    a : int
        The integer for which the modulo needs to be calculated.

    b : int
        The integer by which 'a' will be divided to calculate the modulo.
        Must be non-zero.

    Returns
    -------
    int
        The non-negative modulo of 'a' with respect to 'b'.

    Examples
    --------
    >>> modulo(7, 3)
    1
    >>> modulo(-7, 3)
    2

    Notes
    -----
    This function doesn't work for floating-point numbers.
    """
    return (a % b + b) % b
