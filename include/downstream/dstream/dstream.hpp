#pragma once
#ifndef DOWNSTREAM_DSTREAM_DSTREAM_HPP
#define DOWNSTREAM_DSTREAM_DSTREAM_HPP

#include "./hybrid_0_steady_1_stretched_2/algo.hpp"
#include "./hybrid_0_steady_1_tilted_2/algo.hpp"
#include "./steady/algo.hpp"
#include "./stretched/algo.hpp"
#include "./tilted/algo.hpp"

namespace downstream {
namespace dstream {

using hybrid_0_steady_1_stretched_2_algo =
    dstream_hybrid_0_steady_1_stretched_2::algo;
using hybrid_0_steady_1_tilted_2_algo =
    dstream_hybrid_0_steady_1_tilted_2::algo;
using steady_algo = dstream_steady::algo;
using stretched_algo = dstream_stretched::algo;
using tilted_algo = dstream_tilted::algo;

}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_DSTREAM_HPP
