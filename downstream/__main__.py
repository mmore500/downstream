from downstream.steady_algo import site_selection as steady_site_selection
import time
import random
import math
from downstream.run import run_external_script_parallel
import argparse
import os

def generate_test_cases():
    cases = []
    max_t_all = 8
    max_s = 4096
    for s in range(8, max_s + 1):
        cases.extend((s, t) for t in range(min(2**max_t_all, 2**(s-1))))
        if s > max_t_all + 1:
            max_t = min(2**128, 2**(s-1))
            sample_size = max(10, int(100 * math.log2(s) / math.log2(max_s)))
            cases.extend((s, random.randint(2**max_t_all, max_t-1)) for _ in range(sample_size))
    return cases

def compare_results(external_results, test_cases):
    differences = {}
    for s, t in test_cases:
        key = f"{s},{t}"
        external = external_results.get(key)
        correct = str(steady_site_selection(s, t))
        if str(external) != str(correct):
            print(f"Test {s}, {t} failed: script output '{external}' != correct '{correct}'")
            differences[key] = (external, correct)
    if differences:
        for k, (v, c) in differences.items():
            s, t = map(int, k.split(','))
            # print(f"Test {s}, {t} failed: script output '{v}' != correct '{c}'")
        return False
    else:
        return True

def test_steady_site_selection(executable):
    test_cases = generate_test_cases()
    print(f"Generated {len(test_cases)} test cases")
    start_time = time.time()

    external_results = run_external_script_parallel(test_cases, executable)
    end_time = time.time()
    print(f"External script execution time: {end_time - start_time:.2f} seconds")
    return compare_results(external_results, test_cases)

def main():
    parser = argparse.ArgumentParser(description="Run steady site selection tests")
    parser.add_argument("executable", help="Executable to test (e.g., executable.sh)")
    args = parser.parse_args()

    # Get the full path of the executable
    executable_path = os.path.abspath(args.executable)

    start_time = time.time()
    if test_steady_site_selection(executable_path):
        print("All tests completed successfully.")
    else:
        print("Some tests failed. Please check the output above for details.")
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()