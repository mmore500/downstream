#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

for set in set*; do
    "./${set}/test_all.sh"
done
