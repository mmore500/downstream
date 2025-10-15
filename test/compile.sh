#!/bin/bash

set -e

cd "$(dirname "$0")/.."

echo "CSLC ${CSLC}"

CSLC_ARCH_FLAG="${CSLC_ARCH_FLAG:-wse2}"
echo "CSLC_ARCH_FLAG ${CSLC_ARCH_FLAG}"

# target a 1x1 region of interest
# Every program using memcpy must use a fabric offset of 4,1, and if compiling
# for a simulated fabric, must use a fabric dimension of at least
# width+7,height+2, where width and height are the dimensions of the program.
# These additional PEs are used by memcpy to route data on and off the wafer.
# see https://sdk.cerebras.net/csl/tutorials/gemv-01-complete-program/
# 8x3 because compiler says
# RuntimeError: Fabric dimension must be at least 8-by-3
"${CSLC}" --import-path ./include ./test/layout.csl --arch=${CSLC_ARCH_FLAG} --fabric-dims=8,3 --fabric-offsets=4,1 --channels=1 --memcpy -o out
