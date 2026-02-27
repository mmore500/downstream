#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

for CSLC_ARCH_FLAG in "wse2" "wse3"; do
    echo "CSLC_ARCH_FLAG ${CSLC_ARCH_FLAG}"
    export CSLC_ARCH_FLAG

    ./test.sh 'dstream.circular_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_steady_1_circular_2_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site'
    ./test.sh 'dstream.hybrid_0_tilted_1_circular_2_algo.assign_storage_site'
    ./test.sh 'dstream.steady_algo.assign_storage_site'
    ./test.sh 'dstream.stretched_algo.assign_storage_site'
    ./test.sh 'dstream.tilted_algo.assign_storage_site'
done
