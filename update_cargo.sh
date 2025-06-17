#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

rm -rf /tmp/downstream-cargo-update
mkdir /tmp/downstream-cargo-update
cp -r * /tmp/downstream-cargo-update

pushd /tmp/downstream-cargo-update
cargo update
popd

cp /tmp/downstream-cargo-update/Cargo.toml .

git add Cargo.lock
