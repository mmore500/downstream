from .get_hanoi_val import get_hanoi_val

def get_hanoi_incidence(n: int) -> int:
    """How many times has the hanoi value at index n already been encountered?"""
    return n // 2 ** get_hanoi_val(n)
