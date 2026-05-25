PROJECT := downstream

CXX ?= g++
CXXCLANG ?= clang++
NVCC ?= nvcc
PYTHON ?= python3

CFLAGS_all := -Wall -Wno-unused-function -std=c++20 -I.
CFLAGS_nat := -O3 -DNDEBUG $(CFLAGS_all)
CFLAGS_nat_debug := -g $(CFLAGS_all)

NVCCFLAGS_all := -std=c++20 --expt-relaxed-constexpr -I.
NVCCFLAGS_nat := -O3 -DNDEBUG $(NVCCFLAGS_all)
NVCCFLAGS_nat_debug := -g -G $(NVCCFLAGS_all)

HEADERS := $(shell find include -name '*.hpp')

MAIN_BIN := ./main
CUDA_BIN := ./main_cuda
HIP_BIN := ./main_hip
HIP_SOURCE := ./main_hip.cpp

VENDOR_DIR := vendor
HIPIFY_PERL := $(VENDOR_DIR)/hipify-perl
HIPCPU_DIR := $(VENDOR_DIR)/HIP-CPU
HIPCPU_INCLUDE := $(HIPCPU_DIR)/include
HIPCPU_STAMP := $(HIPCPU_INCLUDE)/hip/hip_runtime.h
HIPIFY_URL := https://raw.githubusercontent.com/ROCm/HIPIFY/develop/bin/hipify-perl
HIPCPU_URL := https://github.com/ROCm/HIP-CPU.git

# HIP-CPU build flags: kernels run on the host CPU via TBB, asserts left live
# so the device-vs-host cross-check in main.cu's destructor actually fires.
HIPFLAGS_all := -Wall -Wno-unused-function -std=c++20 -I. -I$(HIPCPU_INCLUDE)
HIPFLAGS_nat := -O3 -g $(HIPFLAGS_all)
HIPLDFLAGS := -ltbb

ALGOS := \
	dstream.circular_algo \
	dstream.compressing_algo \
	dstream.hybrid_0_circular_11_steady_12_algo \
	dstream.hybrid_0_circular_2_steady_3_algo \
	dstream.hybrid_0_circular_2_tilted_3_algo \
	dstream.hybrid_0_circular_3_steady_4_algo \
	dstream.hybrid_0_circular_5_steady_6_algo \
	dstream.hybrid_0_circular_7_steady_8_algo \
	dstream.hybrid_0_steady_1_circular_2_algo \
	dstream.hybrid_0_steady_1_stretched_2_algo \
	dstream.hybrid_0_steady_1_tilted_2_algo \
	dstream.hybrid_0_steady_1_tilted_2_circular_3_algo \
	dstream.hybrid_0_steady_2_circular_3_algo \
	dstream.hybrid_0_steady_2_tilted_3_algo \
	dstream.hybrid_0_tilted_1_circular_2_algo \
	dstream.hybrid_0_tilted_2_circular_3_algo \
	dstream.hybrid_0_tilted_2_steady_3_algo \
	dstream.steady_algo \
	dstream.sticky_algo \
	dstream.stretched_algo \
	dstream.tilted_algo

default: release validate

.PHONY: all clean check debug debug-cuda default release release-cuda \
        release-hip validate validate-hip vendor
all: release validate release-cuda release-hip validate-hip
debug: CFLAGS_nat := $(CFLAGS_nat_debug)
debug: release
debug-cuda: NVCCFLAGS_nat := $(NVCCFLAGS_nat_debug)
debug-cuda: release-cuda

release: $(MAIN_BIN)
release-cuda: $(CUDA_BIN)
release-hip: $(HIP_BIN)

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

$(MAIN_BIN): $(MAIN_BIN).cpp $(HEADERS)
	@mkdir -p $(dir $@)
	$(CXX) $(CFLAGS_nat) $< -o $@

$(CUDA_BIN): main.cu $(HEADERS)
	@mkdir -p $(dir $@)
	$(NVCC) $(NVCCFLAGS_nat) $< -o $@

validate: debug
	@echo "Running validation tests against $(MAIN_BIN)..."
	@for algo in $(ALGOS); do \
		echo "Validating assign_storage_site for $$algo..."; \
		$(PYTHON) -m downstream.testing.debug_one \
			$(MAIN_BIN) \
			$$algo.assign_storage_site || exit 1; \
		$(PYTHON) -m downstream.testing.validate_one \
			$(MAIN_BIN) \
			$$algo.assign_storage_site || exit 1; \
	done

# --- HIP / HIP-CPU pipeline ----------------------------------------------
# main.cu is translated to a HIP .cpp by hipify-perl, then compiled against
# the header-only HIP-CPU runtime and TBB to produce an executable whose
# kernels run on the host CPU. This gives us real kernel-path coverage in
# environments without a GPU.

vendor: $(HIPIFY_PERL) $(HIPCPU_STAMP)

$(HIPIFY_PERL):
	@mkdir -p $(VENDOR_DIR)
	curl -fsSL $(HIPIFY_URL) -o $@
	chmod +x $@

$(HIPCPU_STAMP):
	@mkdir -p $(VENDOR_DIR)
	git clone --depth 1 $(HIPCPU_URL) $(HIPCPU_DIR)

$(HIP_SOURCE): main.cu $(HIPIFY_PERL)
	$(HIPIFY_PERL) -hip-kernel-execution-syntax $< -o $@

$(HIP_BIN): $(HIP_SOURCE) $(HEADERS) $(HIPCPU_STAMP)
	@mkdir -p $(dir $@)
	$(CXX) $(HIPFLAGS_nat) $(HIP_SOURCE) $(HIPLDFLAGS) -o $@

validate-hip: $(HIP_BIN)
	@echo "Running validation tests against $(HIP_BIN)..."
	@for algo in $(ALGOS); do \
		echo "Validating assign_storage_site for $$algo (HIP-CPU build)..."; \
		$(PYTHON) -m downstream.testing.debug_one \
			$(HIP_BIN) \
			$$algo.assign_storage_site || exit 1; \
		$(PYTHON) -m downstream.testing.validate_one \
			$(HIP_BIN) \
			$$algo.assign_storage_site || exit 1; \
	done

clean:
	@echo "Cleaning build artifacts..."
	rm -f $(MAIN_BIN) $(CUDA_BIN) $(HIP_BIN) $(HIP_SOURCE)
	rm -rf $(VENDOR_DIR)
