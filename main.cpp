#include <cassert>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <format>
#include <string>
#include <string_view>

#include "include/downstream/_auxlib/can_type_fit_value.hpp"
#include "include/downstream/dstream/dstream.hpp"

template<template<typename> typename Algo>
void eval_assign_storage_site(uint64_t S, uint64_t T, uint64_t Smx) {
    namespace downaux = downstream::_auxlib;
    const bool has_capacity = Algo<uint64_t>::has_ingest_capacity(S, T);
    assert(!downaux::can_type_fit_value<uint8_t>(S)
        || !downaux::can_type_fit_value<uint8_t>(T)
        || (Algo<uint8_t>::has_ingest_capacity(S, T) == has_capacity));
    assert(!downaux::can_type_fit_value<uint16_t>(S)
        || !downaux::can_type_fit_value<uint16_t>(T)
        || (Algo<uint16_t>::has_ingest_capacity(S, T) == has_capacity));
    assert(!downaux::can_type_fit_value<uint32_t>(S)
        || !downaux::can_type_fit_value<uint32_t>(T)
        || (Algo<uint32_t>::has_ingest_capacity(S, T) == has_capacity));

    if (has_capacity) {
        const auto maybe_site = Algo<uint64_t>::assign_storage_site(S, T);
        assert(!downaux::can_type_fit_value<uint8_t>(S * Smx)
            || !downaux::can_type_fit_value<uint8_t>(T)
            || (Algo<uint8_t>::assign_storage_site(S, T) == maybe_site));
        assert(!downaux::can_type_fit_value<uint16_t>(S * Smx)
            || !downaux::can_type_fit_value<uint16_t>(T)
            || (Algo<uint16_t>::assign_storage_site(S, T) == maybe_site));
        assert(!downaux::can_type_fit_value<uint32_t>(S * Smx)
            || !downaux::can_type_fit_value<uint32_t>(T)
            || (Algo<uint32_t>::assign_storage_site(S, T) == maybe_site));

        std::cout << (maybe_site ? std::to_string(*maybe_site) : "None");
        std::cout << '\n';
    } else {
        std::cout << '\n';
    }
}

template<typename Algo>
bool is_algo_op(
    const std::string_view op_name, const std::string_view target_name
) {
    return target_name == std::format("{}.{}", Algo::get_algo_name(), op_name);
}

int dispatch_algo_op(const std::string_view target_name) {
    using namespace downstream::dstream;

    uint64_t T, S;
    if (
        is_algo_op<hybrid_0_steady_1_stretched_2_algo>(
        "assign_storage_site", target_name)
    ) while (std::cin >> S >> T) {
        eval_assign_storage_site<hybrid_0_steady_1_stretched_2_algo_>(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_tilted_2_algo>(
        "assign_storage_site", target_name)
    ) while (std::cin >> S >> T) {
        eval_assign_storage_site<hybrid_0_steady_1_tilted_2_algo_>(S, T, 1);
    }
    else if (
        is_algo_op<steady_algo>("assign_storage_site", target_name)
    ) while (std::cin >> S >> T) {
        eval_assign_storage_site<steady_algo_>(S, T, 1);
    }
    else if (
        is_algo_op<stretched_algo>("assign_storage_site", target_name)
    ) while (std::cin >> S >> T) {
        eval_assign_storage_site<stretched_algo_>(S, T, 2);
    }
    else if (
        is_algo_op<tilted_algo>("assign_storage_site", target_name)
    ) while (std::cin >> S >> T) {
        eval_assign_storage_site<tilted_algo_>(S, T, 2);
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
