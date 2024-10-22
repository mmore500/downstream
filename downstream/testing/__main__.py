from signal import SIG_BLOCK, SIGPIPE, signal
import sys

from ._generate_test_cases import generate_test_cases

if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)
    for T, S in generate_test_cases():
        sys.stdout.write(f"{T} {S}\n")
