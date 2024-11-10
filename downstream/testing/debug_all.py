import argparse
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test a downstream implementation against reference.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "command",
        help="The command to test. Example: 'python3 ./my_program'",
    )
    parser.add_argument(
        "--reference",
        default="python3 -O -m downstream",
        help="Reference command to validate against.",
    )
    args = parser.parse_args()

    script = r"""
set -e

for algo in "steady_algo" "stretched_algo" "tilted_algo"; do
    for func in "assign_storage_site" "lookup_ingest_times"; do
        target="${algo}.${func}"
        echo "target=${target}"
        python3 -m downstream.testing.debug_one "$2" "${target}" --reference "$1" | $(which pv && echo "--size $((17*512))" || echo "cat") | grep -v "OK" | tee /dev/stderr | grep "MISMATCH" || echo "ALL OK"
        echo
    done
done
"""

if __name__ == "__main__":
    subprocess.run(
        [
            "bash",
            "-c",
            script,
            sys.argv[0],
            args.reference,
            args.command,
        ],
    )
