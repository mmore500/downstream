#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

./test.sh 'steady_algo.assign_storage_site'
./test.sh 'stretched_algo.assign_storage_site'
./test.sh 'tilted_algo.assign_storage_site'
