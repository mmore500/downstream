#!/bin/bash

set -e

cd "$(dirname "$0")"

ruff --ignore=E501,E402 $@ .
python3 -m nbqa ruff --ignore=E501,E402 $@ .
