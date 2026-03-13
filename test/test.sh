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
    ./zig-out/bin/downstream \
    'dstream.circular_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.compressing_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_2_steady_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_2_tilted_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_3_steady_4_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_5_steady_6_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_7_steady_8_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_11_steady_12_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_circular_2_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_tilted_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_2_tilted_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_1_circular_2_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_2_steady_3_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.steady_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream \
    'dstream.sticky_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.stretched_algo.assign_storage_site'
python3 -m downstream.testing.debug_one \
    ./zig-out/bin/downstream 'dstream.tilted_algo.assign_storage_site'

python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.circular_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.compressing_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_2_steady_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_2_tilted_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_3_steady_4_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_5_steady_6_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_7_steady_8_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_circular_11_steady_12_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_circular_2_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_1_tilted_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_steady_2_tilted_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_1_circular_2_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_2_circular_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.hybrid_0_tilted_2_steady_3_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.steady_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream \
    'dstream.sticky_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.stretched_algo.assign_storage_site'
python3 -m downstream.testing.validate_one \
    ./zig-out/bin/downstream 'dstream.tilted_algo.assign_storage_site'
