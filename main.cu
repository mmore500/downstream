// CUDA entrypoint mirroring main.cpp's CLI: reads `S T` pairs on stdin and
// prints the assigned storage site (or "None" for discard, blank for
// no-capacity), so the same `downstream.testing.validate_one` harness works
// against this binary.
//
// Build:
//   nvcc -std=c++20 --expt-relaxed-constexpr -I. main.cu -o main_cuda
// Validate (one algo):
//   python3 -m downstream.testing.validate_one \
//       ./main_cuda dstream.steady_algo.assign_storage_site
//
// Algorithms whose call graph is annotated DOWNSTREAM_HD (currently
// `dstream_steady`) execute their `_assign_storage_site` on the GPU when a
// CUDA device is available; the device result is asserted equal to the host
// result before printing. Other algorithms and the no-GPU path simply fall
// through to host execution, so the executable still produces correct output
// in environments without a GPU.

#include <cassert>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <optional>
#include <string>
#include <string_view>
#include <type_traits>

#include <cuda_runtime.h>

#include "include/downstream/_auxlib/can_type_fit_value.hpp"
#include "include/downstream/_dispatch_assign_storage_site.hpp"
#include "include/downstream/dstream/steady/_assign_storage_site.hpp"

namespace {

bool cuda_device_available() {
  int n = 0;
  return cudaGetDeviceCount(&n) == cudaSuccess && n > 0;
}

__global__ void steady_assign_kernel(std::uint64_t S, std::uint64_t T,
                                     std::uint64_t *out) {
  *out = downstream::dstream_steady::_assign_storage_site<std::uint64_t>(S, T);
}

std::uint64_t steady_assign_on_device(std::uint64_t S, std::uint64_t T) {
  std::uint64_t *d_out = nullptr;
  cudaMalloc(&d_out, sizeof(std::uint64_t));
  steady_assign_kernel<<<1, 1>>>(S, T, d_out);
  std::uint64_t h_out = 0;
  cudaMemcpy(&h_out, d_out, sizeof(std::uint64_t), cudaMemcpyDeviceToHost);
  cudaFree(d_out);
  return h_out;
}

template <template <typename> typename Algo>
constexpr bool is_steady_algo_v =
    std::is_same_v<Algo<std::uint64_t>,
                   downstream::dstream::steady_algo_<std::uint64_t>>;

}  // namespace

struct CudaEvalAssignStorageSite {
  const bool gpu_available;

  CudaEvalAssignStorageSite() : gpu_available(cuda_device_available()) {}

  template <template <typename> typename Algo>
  void operator()(std::uint64_t S, std::uint64_t T, std::uint64_t Smx) {
    namespace downaux = downstream::_auxlib;
    const bool has_capacity = Algo<std::uint64_t>::has_ingest_capacity(S, T);
    if (!has_capacity) {
      std::cout << '\n';
      return;
    }

    const auto maybe_site = Algo<std::uint64_t>::assign_storage_site(S, T);

    if constexpr (is_steady_algo_v<Algo>) {
      if (gpu_available) {
        const std::uint64_t dev_site = steady_assign_on_device(S, T);
        const std::uint64_t expected = maybe_site.value_or(S);
        assert(dev_site == expected);
        (void)expected;
      }
    }

    // Cross-width invariants, matching the host entrypoint.
    assert(!downaux::can_type_fit_value<std::uint8_t>(S * Smx) ||
           !downaux::can_type_fit_value<std::uint8_t>(T) ||
           (Algo<std::uint8_t>::assign_storage_site(S, T) == maybe_site));
    assert(!downaux::can_type_fit_value<std::uint16_t>(S * Smx) ||
           !downaux::can_type_fit_value<std::uint16_t>(T) ||
           (Algo<std::uint16_t>::assign_storage_site(S, T) == maybe_site));
    assert(!downaux::can_type_fit_value<std::uint32_t>(S * Smx) ||
           !downaux::can_type_fit_value<std::uint32_t>(T) ||
           (Algo<std::uint32_t>::assign_storage_site(S, T) == maybe_site));

    std::cout << (maybe_site ? std::to_string(*maybe_site) : "None") << '\n';
  }
};

int main(int argc, char *argv[]) {
  std::signal(SIGPIPE, SIG_IGN);
  std::ios_base::sync_with_stdio(false);

  const std::string_view target_name(argv[1]);
  CudaEvalAssignStorageSite eval;
  return downstream::dispatch_assign_storage_site(target_name, eval);
}
