# Project-specific settings
PROJECT := downstream

# Compiler settings
CXX ?= g++-12
CXXCLANG ?= clang++
PYTHON ?= python3

# Flags
CFLAGS_all := -Wall -Wno-unused-function -std=c++20 -I.
CFLAGS_nat := -O3 -DNDEBUG $(CFLAGS_all)
CFLAGS_nat_debug := -g $(CFLAGS_all)

# Find all header and source files
HEADERS := $(shell find downstream -name '*.hpp')
TEST_SOURCES := $(shell find test_downstream -name '*.cpp')
TEST_BINS := $(TEST_SOURCES:.cpp=)

# Extract algorithm names for validation
ALGO_DIRS := steady_algo stretched_algo tilted_algo
TEST_NAMES := $(notdir $(TEST_BINS))

# Default target
default: build test

# Main targets
.PHONY: all clean test check debug default build run validate

all: build test validate

debug: CFLAGS_nat := $(CFLAGS_nat_debug)
debug: build

build: $(TEST_BINS)

# C++ syntax check
check:
	@echo "Checking C++20 compatibility..."
	@for file in $(HEADERS); do \
		echo "Checking $$file with GCC..."; \
		$(CXX) $(CFLAGS_nat) -fsyntax-only "$$file" || exit 1; \
		if command -v $(CXXCLANG) > /dev/null 2>&1; then \
			echo "Checking $$file with Clang..."; \
			$(CXXCLANG) $(CFLAGS_nat) -fsyntax-only "$$file" || exit 1; \
		fi \
	done
	@echo "All files pass C++20 syntax check"

# Pattern rule to compile test files
%: %.cpp $(HEADERS)
	@mkdir -p $(dir $@)
	$(CXX) $(CFLAGS_nat) $< -o $@

# Run all tests with validation
validate: build
	@echo "Running validation tests..."
	@for test in $(TEST_BINS); do \
		echo "Validating $$test..."; \
		$(PYTHON) -m downstream.testing.validate_all "$$test" || exit 1; \
	done

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@for bin in $(TEST_BINS); do \
		rm -f $$bin; \
	done

# Run individual test
test-%: build
	@echo "Running test $*..."
	@algo=$$(echo $* | cut -d_ -f2); \
	test_name=$$(echo $* | cut -d_ -f3-); \
	$(PYTHON) -m downstream.testing.validate_all \
		test_downstream/test_dstream/$${algo}_algo/test_$* \
		$${algo}_algo.$$test_name