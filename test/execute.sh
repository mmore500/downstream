#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

echo "CS_PYTHON ${CS_PYTHON}" >/tmp/downstream-csl.log

outfile="$(mktemp)"
echo "outfile ${outfile}" >>/tmp/downstream-csl.log

parallel --pipe -N 8192 -j1 \
    "${CS_PYTHON}" ./test/client.py --algo "$1" --out "${outfile}" \
    >> /tmp/downstream-csl.log 2>&1

cat "${outfile}"
