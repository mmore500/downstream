#!/usr/bin/bash

set -e

cd "$(dirname "$0")"
python3 -m uv pip compile "pyproject.toml" --extra "release" --extra "testing" > requirements.txt
