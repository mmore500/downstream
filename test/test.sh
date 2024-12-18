#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

venv="/tmp/downstream-csl/env"
rm -rf "${venv}"
mkdir -p "${venv}"
python3 -m venv "${venv}"
source "${venv}/bin/activate"

python3 -m pip install uv
python3 -m uv pip install -r requirements.txt

echo "compiling with ${CSLC} CSLC"
./compile.sh > /dev/null 2>&1

echo "executing with ${CS_PYTHON} CS_PYTHON"
# python3 -m downstream.testing.debug_one \
#     ./execute.sh 'steady_algo.assign_storage_site'
# python3 -m downstream.testing.debug_one \
#     ./execute.sh 'stretched_algo.assign_storage_site'
# python3 -m downstream.testing.debug_one \
#     ./execute.sh 'tilted_algo.assign_storage_site'

python3 -m downstream.testing.validate_one \
    ./execute.sh 'steady_algo.assign_storage_site'
# python3 -m downstream.testing.validate_one \
#     ./execute.sh 'stretched_algo.assign_storage_site'
# python3 -m downstream.testing.validate_one \
#     ./execute.sh 'tilted_algo.assign_storage_site'
