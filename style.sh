#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

trap "cargo fmt" EXIT

cargo fmt --check --verbose
