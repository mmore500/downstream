#pragma once
#ifndef DOWNSTREAM_DSTREAM_DSTREAM_HPP
#define DOWNSTREAM_DSTREAM_DSTREAM_HPP

#include <concepts>

#include "../_auxlib/DOWNSTREAM_UINT.hpp"
#include "./circular/algo.hpp"
#include "./compressing/algo.hpp"
#include "./hybrid_0_circular_11_steady_12/algo.hpp"
#include "./hybrid_0_circular_2_steady_3/algo.hpp"
#include "./hybrid_0_circular_2_tilted_3/algo.hpp"
#include "./hybrid_0_circular_3_steady_4/algo.hpp"
#include "./hybrid_0_circular_5_steady_6/algo.hpp"
#include "./hybrid_0_circular_7_steady_8/algo.hpp"
#include "./hybrid_0_steady_1_circular_2/algo.hpp"
#include "./hybrid_0_steady_1_stretched_2/algo.hpp"
#include "./hybrid_0_steady_1_tilted_2/algo.hpp"
#include "./hybrid_0_steady_1_tilted_2_circular_3/algo.hpp"
#include "./hybrid_0_steady_2_circular_3/algo.hpp"
#include "./hybrid_0_steady_2_tilted_3/algo.hpp"
#include "./hybrid_0_tilted_1_circular_2/algo.hpp"
#include "./hybrid_0_tilted_2_circular_3/algo.hpp"
#include "./hybrid_0_tilted_2_steady_3/algo.hpp"
#include "./steady/algo.hpp"
#include "./sticky/algo.hpp"
#include "./stretched/algo.hpp"
#include "./tilted/algo.hpp"

namespace downstream {
namespace dstream {

/** Convenience typedef of compressing algo template. */
template <std::unsigned_integral UINT>
using circular_algo_ = dstream_circular::algo<UINT>;
/** Convenience typedef instantiating steady/stretched hybrid algo obj. */
using circular_algo = circular_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of compressing algo template. */
template <std::unsigned_integral UINT>
using compressing_algo_ = dstream_compressing::algo<UINT>;
/** Convenience typedef instantiating compressing algo obj. */
using compressing_algo = compressing_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_11/steady_12 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_11_steady_12_algo_ =
    dstream_hybrid_0_circular_11_steady_12::algo<UINT>;
/** Convenience typedef instantiating circular_11/steady_12 hybrid algo obj. */
using hybrid_0_circular_11_steady_12_algo =
    hybrid_0_circular_11_steady_12_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_2/steady_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_2_steady_3_algo_ =
    dstream_hybrid_0_circular_2_steady_3::algo<UINT>;
/** Convenience typedef instantiating circular_2/steady_3 hybrid algo obj. */
using hybrid_0_circular_2_steady_3_algo =
    hybrid_0_circular_2_steady_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_2/tilted_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_2_tilted_3_algo_ =
    dstream_hybrid_0_circular_2_tilted_3::algo<UINT>;
/** Convenience typedef instantiating circular_2/tilted_3 hybrid algo obj. */
using hybrid_0_circular_2_tilted_3_algo =
    hybrid_0_circular_2_tilted_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_3/steady_4 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_3_steady_4_algo_ =
    dstream_hybrid_0_circular_3_steady_4::algo<UINT>;
/** Convenience typedef instantiating circular_3/steady_4 hybrid algo obj. */
using hybrid_0_circular_3_steady_4_algo =
    hybrid_0_circular_3_steady_4_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_5/steady_6 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_5_steady_6_algo_ =
    dstream_hybrid_0_circular_5_steady_6::algo<UINT>;
/** Convenience typedef instantiating circular_5/steady_6 hybrid algo obj. */
using hybrid_0_circular_5_steady_6_algo =
    hybrid_0_circular_5_steady_6_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of circular_7/steady_8 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_circular_7_steady_8_algo_ =
    dstream_hybrid_0_circular_7_steady_8::algo<UINT>;
/** Convenience typedef instantiating circular_7/steady_8 hybrid algo obj. */
using hybrid_0_circular_7_steady_8_algo =
    hybrid_0_circular_7_steady_8_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady/circular hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_1_circular_2_algo_ =
    dstream_hybrid_0_steady_1_circular_2::algo<UINT>;
/** Convenience typedef instantiating steady/circular hybrid algo obj. */
using hybrid_0_steady_1_circular_2_algo =
    hybrid_0_steady_1_circular_2_algo_<DOWNSTREAM_UINT>;

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

/** Convenience typedef of steady/tilted/circular hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_1_tilted_2_circular_3_algo_ =
    dstream_hybrid_0_steady_1_tilted_2_circular_3::algo<UINT>;
/** Convenience typedef instantiating steady/tilted/circular hybrid algo obj. */
using hybrid_0_steady_1_tilted_2_circular_3_algo =
    hybrid_0_steady_1_tilted_2_circular_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady_2/circular_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_2_circular_3_algo_ =
    dstream_hybrid_0_steady_2_circular_3::algo<UINT>;
/** Convenience typedef instantiating steady_2/circular_3 hybrid algo obj. */
using hybrid_0_steady_2_circular_3_algo =
    hybrid_0_steady_2_circular_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady_2/tilted_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_steady_2_tilted_3_algo_ =
    dstream_hybrid_0_steady_2_tilted_3::algo<UINT>;
/** Convenience typedef instantiating steady_2/tilted_3 hybrid algo obj. */
using hybrid_0_steady_2_tilted_3_algo =
    hybrid_0_steady_2_tilted_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of tilted/circular hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_tilted_1_circular_2_algo_ =
    dstream_hybrid_0_tilted_1_circular_2::algo<UINT>;
/** Convenience typedef instantiating tilted/circular hybrid algo obj. */
using hybrid_0_tilted_1_circular_2_algo =
    hybrid_0_tilted_1_circular_2_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of tilted_2/circular_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_tilted_2_circular_3_algo_ =
    dstream_hybrid_0_tilted_2_circular_3::algo<UINT>;
/** Convenience typedef instantiating tilted_2/circular_3 hybrid algo obj. */
using hybrid_0_tilted_2_circular_3_algo =
    hybrid_0_tilted_2_circular_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of tilted_2/steady_3 hybrid algo template. */
template <std::unsigned_integral UINT>
using hybrid_0_tilted_2_steady_3_algo_ =
    dstream_hybrid_0_tilted_2_steady_3::algo<UINT>;
/** Convenience typedef instantiating tilted_2/steady_3 hybrid algo obj. */
using hybrid_0_tilted_2_steady_3_algo =
    hybrid_0_tilted_2_steady_3_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of steady algo template. */
template <std::unsigned_integral UINT>
using steady_algo_ = dstream_steady::algo<UINT>;
/** Convenience typedef of steady algo obj. */
using steady_algo = steady_algo_<DOWNSTREAM_UINT>;

/** Convenience typedef of sticky algo template. */
template <std::unsigned_integral UINT>
using sticky_algo_ = dstream_sticky::algo<UINT>;
/** Convenience typedef of sticky algo obj. */
using sticky_algo = sticky_algo_<DOWNSTREAM_UINT>;

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
