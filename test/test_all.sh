#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

./test.sh 'dstream.steady_algo.assign_storage_site'
./test.sh 'dstream.stretched_algo.assign_storage_site'
./test.sh 'dstream.tilted_algo.assign_storage_site'
