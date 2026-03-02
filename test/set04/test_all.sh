#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

for CSLC_ARCH_FLAG in "wse2" "wse3"; do
    echo "CSLC_ARCH_FLAG ${CSLC_ARCH_FLAG}"
    export CSLC_ARCH_FLAG

    ./test.sh 'dstream.hybrid_0_circular_11_steady_12_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_circular_3_steady_4_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_circular_5_steady_6_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_circular_7_steady_8_algo.assign_storage_site'

done
