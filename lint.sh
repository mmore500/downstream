#!/bin/bash
set -e  # Exit on any error

# C++ linting with clang-tidy
echo "Running C++ linting..."
find include/ -name "*.hpp" -o -name "*.cpp" | while read -r file; do
    clang-tidy "$file" -- -std=c++20 -I.
done

echo "All lint checks passed! ✨"