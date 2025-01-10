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
python3 -m downstream --version

zig build

python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.steady_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.stretched_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.tilted_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site'

python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.steady_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.stretched_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.tilted_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site'
