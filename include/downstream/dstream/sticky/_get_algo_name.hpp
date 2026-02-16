#pragma once
#ifndef DOWNSTREAM_DSTREAM_STICKY__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_STICKY__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_sticky {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.sticky_algo"; }

}  // namespace dstream_sticky
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STICKY__GET_ALGO_NAME_HPP
