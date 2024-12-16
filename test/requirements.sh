#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"

python3 -m uv pip compile requirements.in -o requirements.txt
