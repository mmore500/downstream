#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

export RUST_BACKTRACE=1
cargo build
cargo build --release

python3 -m downstream --version

for bin in "target/debug/downstream" "target/release/downstream"; do
# dstream.hybrid_0_steady_1_stretched_2_algo
# dstream.hybrid_0_steady_1_tilted_2_algo
# dstream.tilted_algo
for algo in \
    dstream.steady_algo \
    dstream.stretched_algo \
; do
    echo "Validating ${bin} assign_storage_site for ${algo}..."; \
    python3 -m downstream.testing.debug_one \
        "${bin}" \
        "${algo}.assign_storage_site" || exit 1; \
    python3 -m downstream.testing.validate_one \
        "${bin}" \
        "${algo}.assign_storage_site" || exit 1; \
done
done
