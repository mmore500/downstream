#!/usr/bin/env bash

set -e

printf "Smoke testing python3 -O -m downstream $2... "
: | python3 -O -m downstream $2
echo 8 0 | python3 -O -m downstream $2

printf "Smoke testing $1 $2... "
: | $1 $2
echo 8 0 | $1 $2

echo "Comparing $1 $2 to python3 -O -m downstream $2..."
badline="$( \
    cmp <( \
            python3 -O -m downstream.testing \
            | pv --size $((840*1024)) \
            | python3 -O -m downstream $2 \
        ) \
        <( \
            python3 -O -m downstream.testing \
            | $1 $2 \
        ) \
    | awk '{print $NF}' \
)"

if [ -n "${badline}" ]; then
    sleep 1
    echo "Tests failed on line ${badline}"
    inline=$(python3 -m downstream.testing | head -n "${badline}" | tail -n 1)
    S=$(echo "${inline}" | cut -d ' ' -f 1)
    T=$(echo "${inline}" | cut -d ' ' -f 2)
    echo "S=${S}, T=${T}"

    aline="$(python3 -m downstream.testing | python3 -m downstream $2 | head -n "${badline}" | tail -n 1)"
    echo "python3 -m downstream $2"
    echo ">>> ${aline}"

    bline="$(python3 -m downstream.testing | $1 $2 | head -n "${badline}" | tail -n 1)"
    echo "$1 $2"
    echo ">>> ${bline}"

    exit 1
else
    echo "Test passed!"
    exit 0
fi
