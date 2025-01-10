#pragma once
#ifndef DOWNSTREAM_DSTREAM_DSTREAM_HPP
#define DOWNSTREAM_DSTREAM_DSTREAM_HPP

@include <concepts>

#include "../auxlib/DOWNSTREAM_UINT.hpp"
#include "./hybrid_0_steady_1_stretched_2/algo.hpp"
#include "./hybrid_0_steady_1_tilted_2/algo.hpp"
#include "./steady/algo.hpp"
#include "./stretched/algo.hpp"
#include "./tilted/algo.hpp"

namespace downstream {
namespace dstream {

template <std::unsigned_integral UINT>
using hybrid_0_steady_1_stretched_2_algo_ =
    dstream_hybrid_0_steady_1_stretched_2::algo<UINT>;
using hybrid_0_steady_1_stretched_2_algo =
    hybrid_0_steady_1_stretched_2_algo_<DOWNSTREAM_UINT>;

template <std::unsigned_integral UINT>
using hybrid_0_steady_1_tilted_2_algo_ =
    dstream_hybrid_0_steady_1_tilted_2::algo<UINT>;
using hybrid_0_steady_1_tilted_2_algo =
    hybrid_0_steady_1_tilted_2_algo_<DOWNSTREAM_UINT>;

template <std::unsigned_integral UINT>
using steady_algo_ = dstream_steady::algo<UINT>;
using steady_algo = steady_algo_<DOWNSTREAM_UINT>;

template <std::unsigned_integral UINT>
using stretched_algo_ = dstream_stretched::algo<UINT>;
using stretched_algo = stretched_algo_<DOWNSTREAM_UINT>;

template <std::unsigned_integral UINT>
using tilted_algo_ = dstream_tilted::algo<UINT>;
using tilted_algo = tilted_algo_<DOWNSTREAM_UINT>;

}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_DSTREAM_HPP
