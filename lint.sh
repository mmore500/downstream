#!/bin/bash

set -e

cd "$(dirname "$0")"

python3 -m nbqa ruff --ignore=E501,E402 $@ .
