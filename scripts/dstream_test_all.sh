#!/usr/bin/env bash

set -e

rm -rf /tmp/dstream
mkdir -p /tmp/dstream

for algo in "steady_algo" "stretched_algo" "tilted_algo"; do
    for func in "assign_storage_site" "lookup_ingest_times"; do
        target="${algo}.${func}"
        echo "target=${target}"
        (\
            dstream_test_one.sh "$1" "${target}" >/dev/null \
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
