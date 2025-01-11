#include <cassert>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <string>
#include <string_view>

#include "include/downstream/auxlib/can_type_fit_value.hpp"
#include "include/downstream/dstream/dstream.hpp"

namespace {

template<template<typename> typename Algo>
void process_single_input(uint64_t S, uint64_t T) {
    namespace downaux = downstream::auxlib;
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
        // assert(!downaux::can_type_fit_value<uint8_t>(S)
        //     || !downaux::can_type_fit_value<uint8_t>(T)
        //     || (Algo<uint8_t>::assign_storage_site(S, T) == maybe_site));
        // assert(!downaux::can_type_fit_value<uint16_t>(S)
        //     || !downaux::can_type_fit_value<uint16_t>(T)
        //     || (Algo<uint16_t>::assign_storage_site(S, T) == maybe_site));
        assert(!downaux::can_type_fit_value<uint32_t>(S)
            || !downaux::can_type_fit_value<uint32_t>(T)
            || (Algo<uint32_t>::assign_storage_site(S, T) == maybe_site));

        std::cout << (maybe_site ? std::to_string(*maybe_site) : "None");
        std::cout << '\n';
    } else {
        std::cout << '\n';
    }
}

bool process_algorithm(const std::string_view target_function) {
    using namespace downstream::dstream;

    uint64_t T, S;
    while (std::cin >> S >> T) {
        if (target_function == "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site") {
            process_single_input<hybrid_0_steady_1_stretched_2_algo_>(S, T);
        }
        else if (target_function == "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site") {
            process_single_input<hybrid_0_steady_1_tilted_2_algo_>(S, T);
        }
        else if (target_function == "dstream.steady_algo.assign_storage_site") {
            process_single_input<steady_algo_>(S, T);
        }
        else if (target_function == "dstream.stretched_algo.assign_storage_site") {
            process_single_input<stretched_algo_>(S, T);

        }
        else if (target_function == "dstream.tilted_algo.assign_storage_site") {
            process_single_input<tilted_algo_>(S, T);
        }
        else {
            std::cerr << "Error: Unknown algorithm function: " << target_function << '\n';
            return false;
        }
    }
    return true;
}

}  // namespace

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN); // Ignore broken pipe signals
    std::ios_base::sync_with_stdio(false); // Disable synchronization with C stdio for performance

    std::string_view target_function(argv[1]);
    if (!process_algorithm(target_function)) {
        return 1;
    }

    return 0;
}
