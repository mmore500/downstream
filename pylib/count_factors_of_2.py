def count_factors_of_2(number: int) -> int:
    """Counts the number of factors of 2 in a given integer using bitwise operations.

    Returns
    -------
    int
        The number of factors of 2.

    Examples
    --------
    >>> count_factors_of_2(12)
    2
    >>> count_factors_of_2(1024)
    10
    """
    if number == 0:
        return 0
    else:
        return (number & -number).bit_length() - 1
