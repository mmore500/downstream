#!/bin/bash

set -euo pipefail

set="$(basename "$(realpath "$(dirname "$0")")")"
echo "testing ${set}" > /tmp/downstream-csl.log
cd "$(dirname "$0")/../.."

echo "CS_PYTHON ${CS_PYTHON}" >> /tmp/downstream-csl.log

outfile="$(mktemp)"
echo "outfile ${outfile}" >>/tmp/downstream-csl.log

mkdir -p ~/.parallel || :; touch ~/.parallel/will-cite || :;
parallel --pipe -N 2048 -j1 \
    "${CS_PYTHON}" ./test/${set}/client.py --algo "$1" --out "${outfile}" \
    >> /tmp/downstream-csl.log 2>&1

cat "${outfile}"
