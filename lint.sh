#!/bin/bash
set -euo pipefail  # Exit on any error

cd "$(dirname "$0")"

# C++ linting with clang-tidy
echo "Running C++ linting..."
find include/ -name "*.hpp" -o -name "*.cpp" | while read -r file; do
    clang-tidy "$file" -- -std=c++20 -I.
done

echo "All lint checks passed! ✨"
