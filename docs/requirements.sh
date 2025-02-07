#!/bin/bash

set -e

cd "$(dirname "$0")"
python3 -m uv pip compile "requirements.in" --python-version=3.10 > requirements.txt