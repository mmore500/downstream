// Brief CUDA example: call dstream_steady::_assign_storage_site on device.
//
// Build:
//   nvcc -std=c++20 --expt-relaxed-constexpr -I. example.cu -o example
// Run:
//   ./example

#include <cstdint>
#include <cstdio>

#include "include/downstream/dstream/steady/_assign_storage_site.hpp"

__global__ void assign_kernel(
    std::uint64_t S, std::uint64_t T0, std::uint64_t N, std::uint64_t* out
) {
    const std::uint64_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= N) return;
    // Returns S to signal "discard" (no site assigned).
    out[i] = downstream::dstream_steady::_assign_storage_site<std::uint64_t>(
        S, T0 + i
    );
}

int main() {
    constexpr std::uint64_t S = 16;  // buffer size (power of two)
    constexpr std::uint64_t N = 32;  // number of ingest steps to evaluate

    std::uint64_t* d_out;
    cudaMalloc(&d_out, N * sizeof(std::uint64_t));

    assign_kernel<<<1, N>>>(S, 0, N, d_out);

    std::uint64_t h_out[N];
    cudaMemcpy(h_out, d_out, N * sizeof(std::uint64_t), cudaMemcpyDeviceToHost);
    cudaFree(d_out);

    for (std::uint64_t T = 0; T < N; ++T) {
        if (h_out[T] == S) std::printf("T=%2lu -> discard\n", T);
        else               std::printf("T=%2lu -> site %lu\n", T, h_out[T]);
    }
    return 0;
}
