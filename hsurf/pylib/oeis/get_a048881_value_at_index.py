# see https://oeis.org/A048881
def get_a048881_value_at_index(n: int) -> int:
    # Chai Wah Wu, Nov 15 2022
    return (n + 1).bit_count() - 1
