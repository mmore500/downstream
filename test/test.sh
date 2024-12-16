#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

venv="/tmp/downstream-zig/env"
rm -rf "${venv}"
mkdir -p "${venv}"
python3 -m venv "${venv}"
source "${venv}/bin/activate"

python3 -m pip install uv
python3 -m uv pip install -r test/requirements.txt

zig build

python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'steady_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'stretched_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'tilted_algo.assign_storage_site'

python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'steady_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'stretched_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'tilted_algo.assign_storage_site'
