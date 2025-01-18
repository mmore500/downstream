#pragma once
#ifndef DOWNSTREAM_DSTREAM_DSTREAM_HPP
#define DOWNSTREAM_DSTREAM_DSTREAM_HPP

#include <concepts>

#include "../_auxlib/DOWNSTREAM_UINT.hpp"
#include "./hybrid_0_steady_1_stretched_2/algo.hpp"
#include "./hybrid_0_steady_1_tilted_2/algo.hpp"
#include "./steady/algo.hpp"
#include "./stretched/algo.hpp"
#include "./tilted/algo.hpp"

namespace downstream {
namespace dstream {

/** Convenience typedef of steady/stretched hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_1_stretched_2_algo_ =
    dstream_hybrid_0_steady_1_stretched_2::algo<UINT>;
/** Convenience typedef instantiating steady/stretched hybrid algo obj. */
using hybrid_0_steady_1_stretched_2_algo =
    hybrid_0_steady_1_stretched_2_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady/tilted hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_1_tilted_2_algo_ =
    dstream_hybrid_0_steady_1_tilted_2::algo<UINT>;
/** Convenience typedef instantiating steady/tilted hybrid algo obj. */
using hybrid_0_steady_1_tilted_2_algo =
    hybrid_0_steady_1_tilted_2_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady algo template. */
template <std::unsigned_integral UINT>
using steady_algo_ = dstream_steady::algo<UINT>;
/** Convenience typedef of steady algo obj. */
using steady_algo = steady_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of stretched algo template. */
template <std::unsigned_integral UINT>
using stretched_algo_ = dstream_stretched::algo<UINT>;
/** Convenience typedef of stretched algo obj. */
using stretched_algo = stretched_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of tilted algo template. */
template <std::unsigned_integral UINT>
using tilted_algo_ = dstream_tilted::algo<UINT>;
/** Convenience typedef of tilted algo obj. */
using tilted_algo = tilted_algo_<DOWNSTREAM_UINT>;

}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_DSTREAM_HPP
