import math


def round_to_one_sigfig(n: int):
    if n == 0:
        return 0

    # Calculate the order of magnitude of the number
    magnitude = math.floor(math.log10(abs(n)))

    # Divide the number by 10 to the power of magnitude, round it,
    # and then multiply it back
    return round(n / 10**magnitude) * 10**magnitude
