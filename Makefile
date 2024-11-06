# Project-specific settings
PROJECT := downstream

# Flags to use regardless of compiler
CFLAGS_all := -Wall -Wno-unused-function -std=c++20 -I.

# Native compiler information
CXX ?= g++-12
CXXCLANG ?= clang++
CFLAGS_nat := -O3 -DNDEBUG $(CFLAGS_all)
CFLAGS_nat_debug := -g $(CFLAGS_all)

# Find all header files and test files
HEADERS := $(shell find downstream -name '*.hpp')
TEST_SOURCES := $(shell find test_downstream -name '*.cpp')
TEST_BINS := $(TEST_SOURCES:.cpp=)

default: check
all: check run

debug: CFLAGS_nat := $(CFLAGS_nat_debug)
debug: check

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

run: $(TEST_BINS)
	@echo "Running validator..."
	@for test in $(TEST_BINS); do \
		echo "Testing $$test..."; \
		python3 -m downstream.testing.validate_one "./$$test" steady_algo.assign_storage_site || exit 1; \
	done

clean:
	@for bin in $(TEST_BINS); do \
		rm -f $$bin; \
	done

test: check run

.PHONY: all clean test check debug default run