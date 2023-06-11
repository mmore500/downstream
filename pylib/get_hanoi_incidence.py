from .get_hanoi_value import get_hanoi_value

def get_hanoi_incidence(n: int) -> int:
    """How many times has the hanoi value at index n already been encountered?"""
    return n // 2 ** get_hanoi_value(n)
