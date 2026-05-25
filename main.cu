#include <cassert>
#include <csignal>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <format>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

#include <cuda_runtime.h>

#include "include/downstream/_auxlib/can_type_fit_value.hpp"
#include "include/downstream/dstream/dstream.hpp"

void require_cuda_device() {
    int n = 0;
    if (cudaGetDeviceCount(&n) != cudaSuccess || n <= 0) {
        std::cerr << "No CUDA device available; aborting.\n";
        std::exit(1);
    }
}

template <template <typename> typename Algo>
__global__ void assign_kernel(
    std::size_t N,
    const std::uint64_t* S,
    const std::uint64_t* T,
    std::uint64_t* out
) {
    const std::size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= N) return;
    if (!Algo<std::uint64_t>::has_ingest_capacity(S[i], T[i])) {
        out[i] = S[i];  // sentinel: no capacity
        return;
    }
    out[i] = Algo<std::uint64_t>::_assign_storage_site(S[i], T[i]);
}

template <template <typename> typename Algo>
struct CudaEvalAssignStorageSite {
    std::vector<std::uint64_t> Ss;
    std::vector<std::uint64_t> Ts;
    std::vector<std::uint64_t> host_results;  // sentinel value = S (no-capacity/discard)
    std::vector<unsigned char> has_capacity;

    CudaEvalAssignStorageSite() { require_cuda_device(); }

    void operator()(std::uint64_t S, std::uint64_t T, std::uint64_t Smx) {
        const bool cap = Algo<std::uint64_t>::has_ingest_capacity(S, T);
        assert(!downstream::_auxlib::can_type_fit_value<std::uint8_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint8_t>(T)
            || (Algo<std::uint8_t>::has_ingest_capacity(S, T) == cap));
        assert(!downstream::_auxlib::can_type_fit_value<std::uint16_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint16_t>(T)
            || (Algo<std::uint16_t>::has_ingest_capacity(S, T) == cap));
        assert(!downstream::_auxlib::can_type_fit_value<std::uint32_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint32_t>(T)
            || (Algo<std::uint32_t>::has_ingest_capacity(S, T) == cap));

        std::uint64_t result = S;  // sentinel: no-capacity or discard
        if (cap) {
            const auto maybe_site = Algo<std::uint64_t>::assign_storage_site(S, T);
            assert(!downstream::_auxlib::can_type_fit_value<std::uint8_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint8_t>(T)
                || (Algo<std::uint8_t>::assign_storage_site(S, T) == maybe_site));
            assert(!downstream::_auxlib::can_type_fit_value<std::uint16_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint16_t>(T)
                || (Algo<std::uint16_t>::assign_storage_site(S, T) == maybe_site));
            assert(!downstream::_auxlib::can_type_fit_value<std::uint32_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint32_t>(T)
                || (Algo<std::uint32_t>::assign_storage_site(S, T) == maybe_site));
            if (maybe_site) result = *maybe_site;
        }

        Ss.push_back(S);
        Ts.push_back(T);
        host_results.push_back(result);
        has_capacity.push_back(cap ? 1 : 0);
    }

    ~CudaEvalAssignStorageSite() {
        const std::size_t N = Ss.size();

        if (N > 0) {
            std::uint64_t* d_S = nullptr;
            std::uint64_t* d_T = nullptr;
            std::uint64_t* d_out = nullptr;
            const std::size_t bytes = N * sizeof(std::uint64_t);
            cudaMalloc(&d_S, bytes);
            cudaMalloc(&d_T, bytes);
            cudaMalloc(&d_out, bytes);
            cudaMemcpy(d_S, Ss.data(), bytes, cudaMemcpyHostToDevice);
            cudaMemcpy(d_T, Ts.data(), bytes, cudaMemcpyHostToDevice);

            constexpr int threads = 256;
            const int blocks = static_cast<int>((N + threads - 1) / threads);
            assign_kernel<Algo><<<blocks, threads>>>(N, d_S, d_T, d_out);

            std::vector<std::uint64_t> dev_results(N);
            cudaMemcpy(dev_results.data(), d_out, bytes, cudaMemcpyDeviceToHost);
            cudaFree(d_S);
            cudaFree(d_T);
            cudaFree(d_out);

            for (std::size_t i = 0; i < N; ++i) {
                assert(dev_results[i] == host_results[i]);
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

template<typename Algo>
bool is_algo_op(
    const std::string_view op_name, const std::string_view target_name
) {
    return target_name == std::format("{}.{}", Algo::get_algo_name(), op_name);
}

int dispatch_algo_op(const std::string_view target_name) {
    using namespace downstream::dstream;

    std::uint64_t T, S;
    if (
        is_algo_op<circular_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<circular_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<compressing_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<compressing_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_11_steady_12_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_11_steady_12_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_2_steady_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_2_steady_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_2_tilted_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_2_tilted_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_3_steady_4_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_3_steady_4_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_5_steady_6_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_5_steady_6_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_7_steady_8_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_circular_7_steady_8_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_circular_2_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_1_circular_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_stretched_2_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_1_stretched_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_tilted_2_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_1_tilted_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_tilted_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_1_tilted_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_2_tilted_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_steady_2_tilted_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_1_circular_2_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_tilted_1_circular_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_tilted_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_2_steady_3_algo>(
        "assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<hybrid_0_tilted_2_steady_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<steady_algo>("assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<steady_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<sticky_algo>("assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<sticky_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<stretched_algo>("assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<stretched_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 2);
    }
    else if (
        is_algo_op<tilted_algo>("assign_storage_site", target_name)
    ) {
        CudaEvalAssignStorageSite<tilted_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 2);
    }
    else {
        std::cerr << "Unknown algorithm op: " << target_name << '\n';
        return 1;
    }
    return 0;
}

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN); // Ignore broken pipe signals
    std::ios_base::sync_with_stdio(false); // Disable sync w/ C stdio for perf

    std::string_view target_name(argv[1]);
    return dispatch_algo_op(target_name);
}
