#pragma once
#ifndef DOWNSTREAM_DSTREAM_CIRCULAR__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_CIRCULAR__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_circular {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.circular_algo"; }

}  // namespace dstream_circular
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_CIRCULAR__GET_ALGO_NAME_HPP
