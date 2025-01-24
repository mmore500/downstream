#pragma once
#ifndef DOWNSTREAM_DSTREAM_STEADY__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_STEADY__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_steady {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.steady_algo"; }

}  // namespace dstream_steady
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STEADY__GET_ALGO_NAME_HPP
