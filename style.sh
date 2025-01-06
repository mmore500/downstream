#!/bin/bash
set -e  # Exit on any error

# Format C++ files
echo "Formatting C++ files..."
find downstream/ -name "*.hpp" -o -name "*.cpp" | while read -r file; do
    clang-format -style=file -i "$file"
done

# Check for trailing whitespace and missing final newlines
echo "Checking for whitespace issues..."
! find . -type f \( -name "*.hpp" -o -name "*.cpp" \) -exec grep -l "[[:blank:]]$" {} \;

# Ensure all files end with newline
echo "Checking for final newlines..."
! find . -type f \( -name "*.hpp" -o -name "*.cpp" \) -print0 | \
    while IFS= read -r -d '' file; do
        if [ -s "$file" ] && [ "$(tail -c1 "$file"; echo x)" != $'\nx' ]; then
            echo "No newline at end of $file"
            exit 1
        fi
    done

echo "All style checks passed! ✨"