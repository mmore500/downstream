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
// `CudaEvalAssignStorageSite` buffers every per-pair invocation from the
// shared dispatcher and flushes once at destruction. When a CUDA device is
// available and the dispatched algo is `dstream_steady` (whose call graph is
// DOWNSTREAM_CUDA_HD-annotated), the flush issues a single bulk kernel launch
// (N threads, one H2D copy, one D2H copy) and asserts the device result
// matches the host result before printing. Other algorithms and the no-GPU
// path simply print the buffered host results, so the binary remains
// output-equivalent to ./main in environments without a GPU.

#include <cassert>
#include <csignal>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <optional>
#include <string>
#include <string_view>
#include <type_traits>
#include <vector>

#include <cuda_runtime.h>

#include "impl/_dispatch_assign_storage_site.hpp"
#include "include/downstream/_auxlib/can_type_fit_value.hpp"
#include "include/downstream/dstream/steady/_assign_storage_site.hpp"

namespace {

bool cuda_device_available() {
  int n = 0;
  return cudaGetDeviceCount(&n) == cudaSuccess && n > 0;
}

__global__ void steady_assign_kernel(std::size_t N, const std::uint64_t *S,
                                     const std::uint64_t *T,
                                     std::uint64_t *out) {
  const std::size_t i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= N) return;
  out[i] = downstream::dstream_steady::_assign_storage_site<std::uint64_t>(
      S[i], T[i]);
}

template <template <typename> typename Algo>
constexpr bool is_steady_algo_v =
    std::is_same_v<Algo<std::uint64_t>,
                   downstream::dstream::steady_algo_<std::uint64_t>>;

}  // namespace

struct CudaEvalAssignStorageSite {
  const bool gpu_available;
  bool is_steady = false;
  std::vector<std::uint64_t> Ss;
  std::vector<std::uint64_t> Ts;
  std::vector<std::uint64_t> host_results;  // sentinel = S (no-capacity/discard)
  std::vector<unsigned char> has_capacity;

  CudaEvalAssignStorageSite() : gpu_available(cuda_device_available()) {}

  template <template <typename> typename Algo>
  void operator()(std::uint64_t S, std::uint64_t T, std::uint64_t Smx) {
    namespace downaux = downstream::_auxlib;

    if constexpr (is_steady_algo_v<Algo>) is_steady = true;

    const bool cap = Algo<std::uint64_t>::has_ingest_capacity(S, T);
    assert(!downaux::can_type_fit_value<std::uint8_t>(S) ||
           !downaux::can_type_fit_value<std::uint8_t>(T) ||
           (Algo<std::uint8_t>::has_ingest_capacity(S, T) == cap));
    assert(!downaux::can_type_fit_value<std::uint16_t>(S) ||
           !downaux::can_type_fit_value<std::uint16_t>(T) ||
           (Algo<std::uint16_t>::has_ingest_capacity(S, T) == cap));
    assert(!downaux::can_type_fit_value<std::uint32_t>(S) ||
           !downaux::can_type_fit_value<std::uint32_t>(T) ||
           (Algo<std::uint32_t>::has_ingest_capacity(S, T) == cap));

    std::uint64_t result = S;  // sentinel: no-capacity or discard
    if (cap) {
      const auto maybe_site = Algo<std::uint64_t>::assign_storage_site(S, T);
      assert(!downaux::can_type_fit_value<std::uint8_t>(S * Smx) ||
             !downaux::can_type_fit_value<std::uint8_t>(T) ||
             (Algo<std::uint8_t>::assign_storage_site(S, T) == maybe_site));
      assert(!downaux::can_type_fit_value<std::uint16_t>(S * Smx) ||
             !downaux::can_type_fit_value<std::uint16_t>(T) ||
             (Algo<std::uint16_t>::assign_storage_site(S, T) == maybe_site));
      assert(!downaux::can_type_fit_value<std::uint32_t>(S * Smx) ||
             !downaux::can_type_fit_value<std::uint32_t>(T) ||
             (Algo<std::uint32_t>::assign_storage_site(S, T) == maybe_site));
      if (maybe_site) result = *maybe_site;
    }

    Ss.push_back(S);
    Ts.push_back(T);
    host_results.push_back(result);
    has_capacity.push_back(cap ? 1 : 0);
  }

  ~CudaEvalAssignStorageSite() {
    const std::size_t N = Ss.size();

    if (is_steady && gpu_available && N > 0) {
      std::uint64_t *d_S = nullptr;
      std::uint64_t *d_T = nullptr;
      std::uint64_t *d_out = nullptr;
      const std::size_t bytes = N * sizeof(std::uint64_t);
      cudaMalloc(&d_S, bytes);
      cudaMalloc(&d_T, bytes);
      cudaMalloc(&d_out, bytes);
      cudaMemcpy(d_S, Ss.data(), bytes, cudaMemcpyHostToDevice);
      cudaMemcpy(d_T, Ts.data(), bytes, cudaMemcpyHostToDevice);

      constexpr int threads = 256;
      const int blocks = static_cast<int>((N + threads - 1) / threads);
      steady_assign_kernel<<<blocks, threads>>>(N, d_S, d_T, d_out);

      std::vector<std::uint64_t> dev_results(N);
      cudaMemcpy(dev_results.data(), d_out, bytes, cudaMemcpyDeviceToHost);
      cudaFree(d_S);
      cudaFree(d_T);
      cudaFree(d_out);

      for (std::size_t i = 0; i < N; ++i) {
        assert(dev_results[i] == host_results[i]);
        (void)dev_results[i];
      }
    }

    for (std::size_t i = 0; i < N; ++i) {
      if (!has_capacity[i]) {
        std::cout << '\n';
      } else if (host_results[i] == Ss[i]) {
        std::cout << "None\n";
      } else {
        std::cout << host_results[i] << '\n';
      }
    }
    std::cout.flush();
  }
};

int main(int argc, char *argv[]) {
  std::signal(SIGPIPE, SIG_IGN);
  std::ios_base::sync_with_stdio(false);

  const std::string_view target_name(argv[1]);
  CudaEvalAssignStorageSite eval;
  return downstream::dispatch_assign_storage_site(target_name, eval);
}
