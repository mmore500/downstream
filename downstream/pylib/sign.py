def sign(x: int) -> int:
    """Calculate the sign of an integer.

    This function takes an integer input and returns:
    - 1 if the number is positive,
    - 0 if the number is zero, or
    - -1 if the number is negative.

    Returns
    -------
    int
        The sign of the input integer (1, 0, or -1).

    Examples
    --------
    >>> sign(10)
    1
    >>> sign(0)
    0
    >>> sign(-1)
    -1
    """
    return (x > 0) - (x < 0)
