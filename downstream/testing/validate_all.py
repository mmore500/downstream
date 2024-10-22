import subprocess
import sys


_script = r"""
set -e

rm -rf /tmp/dstream
mkdir -p /tmp/dstream

for algo in "steady_algo" "stretched_algo" "tilted_algo"; do
    for func in "assign_storage_site" "lookup_ingest_times"; do
        target="${algo}.${func}"
        echo "target=${target}"
        (\
            python3 -m downstream.testing.validate_one "$1" "${target}" >/dev/null \
            || touch "/tmp/dstream/${target}" \
        ) &
    done
done

wait

if ls /tmp/dstream/* 1> /dev/null 2>&1; then
    echo "Tests failed!"
    (cd /tmp/dstream && ls *)
    exit 1
else
    echo "All tests passed!"
    exit 0
fi

rm -f /tmp/dstream
"""

if __name__ == "__main__":
    subprocess.run(
        [
            "bash",
            "-c",
            _script,
            *sys.argv
        ],
    )
