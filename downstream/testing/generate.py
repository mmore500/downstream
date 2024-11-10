import itertools as it
import random
from signal import SIG_BLOCK, SIGPIPE, signal
import sys
import typing


def generate_test_cases() -> typing.Iterable[typing.Tuple[int, int]]:
    rand = random.Random(1)
    for s, T in it.product(range(21), range(4096)):
        S = 1 << s
        capacity_bound = 1 << min(S, 32)
        yield S, T
        if T < 100:
            yield S, rand.randint(0, capacity_bound - 1)
            yield S, rand.randint(0, 2**32 - 1)


if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)
    for T, S in generate_test_cases():
        sys.stdout.write(f"{T} {S}\n")