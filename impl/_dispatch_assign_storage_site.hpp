#pragma once
#ifndef DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP

#include <cstdint>
#include <format>
#include <iostream>
#include <string_view>

#include "include/downstream/dstream/dstream.hpp"

namespace downstream {

template <typename Algo>
inline bool is_algo_op(const std::string_view op_name,
                       const std::string_view target_name) {
  return target_name == std::format("{}.{}", Algo::get_algo_name(), op_name);
}

template <template <template <typename> typename> typename EvalT>
int dispatch_assign_storage_site(const std::string_view target_name) {
    using namespace downstream::dstream;
    std::uint64_t T, S;
    if (
        is_algo_op<circular_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<circular_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<compressing_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<compressing_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_11_steady_12_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_11_steady_12_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_2_steady_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_2_steady_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_2_tilted_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_2_tilted_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_3_steady_4_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_3_steady_4_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_5_steady_6_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_5_steady_6_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_circular_7_steady_8_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_circular_7_steady_8_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_circular_2_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_1_circular_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_stretched_2_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_1_stretched_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_tilted_2_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_1_tilted_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_1_tilted_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_1_tilted_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_steady_2_tilted_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_steady_2_tilted_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_1_circular_2_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_tilted_1_circular_2_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_2_circular_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_tilted_2_circular_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<hybrid_0_tilted_2_steady_3_algo>(
        "assign_storage_site", target_name)
    ) {
        EvalT<hybrid_0_tilted_2_steady_3_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<steady_algo>("assign_storage_site", target_name)
    ) {
        EvalT<steady_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<sticky_algo>("assign_storage_site", target_name)
    ) {
        EvalT<sticky_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 1);
    }
    else if (
        is_algo_op<stretched_algo>("assign_storage_site", target_name)
    ) {
        EvalT<stretched_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 2);
    }
    else if (
        is_algo_op<tilted_algo>("assign_storage_site", target_name)
    ) {
        EvalT<tilted_algo_> eval;
        while (std::cin >> S >> T) eval(S, T, 2);
    }
    else {
        std::cerr << "Unknown algorithm op: " << target_name << '\n';
        return 1;
    }
    return 0;
}

}  // namespace downstream

#endif  // DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP
