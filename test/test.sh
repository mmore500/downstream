#!/usr/bin/env bash

set -euo pipefail

echo "testing $1"
echo "set $(dirname "$1")"
echo "algo $(basename "$1")"

cd "$(dirname "${BASH_SOURCE[0]}")"

"./$(dirname "${1}")/test.sh" "$(basename "${1}")"
