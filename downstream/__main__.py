import subprocess
import json
from steady_site_selection import steady_site_selection
import time
import multiprocessing as mp
from itertools import repeat
import random
import math
import sys

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

def run_external_script_batch(args):
    batch, script_path = args
    cmd = [script_path, "--batch"] + [item for s, t in batch for item in ["-S", str(s), "-T", str(t)]]
    result = subprocess.run([sys.executable] + cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def run_external_script_parallel(test_cases, batch_size=500, script_path="steady_site_selection.py"):
    batches = [test_cases[i:i+batch_size] for i in range(0, len(test_cases), batch_size)]

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(run_external_script_batch, zip(batches, repeat(script_path)))

    return {k: v for d in results for k, v in d.items()}

def compare_results(external_results, test_cases):
    differences = {}
    for s, t in test_cases:
        key = f"{s},{t}"
        external = external_results.get(key)
        correct = str(steady_site_selection(s, t))
        if external != correct:
            differences[key] = (external, correct)

    if differences:
        for k, (v, c) in differences.items():
            s, t = map(int, k.split(','))
            print(f"Test {s}, {t} failed: script output '{v}' != correct '{c}'")
        return False
    else:
        print("All tests passed!")
        return True

def test_steady_site_selection():
    test_cases = generate_test_cases()
    print(f"Generated {len(test_cases)} test cases")

    start_time = time.time()
    external_results = run_external_script_parallel(test_cases)
    end_time = time.time()
    print(f"External script execution time: {end_time - start_time:.2f} seconds")

    return compare_results(external_results, test_cases)

def main():
    start_time = time.time()
    if test_steady_site_selection():
        print("All tests completed successfully.")
    else:
        print("Some tests failed. Please check the output above for details.")
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()