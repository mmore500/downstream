#pragma once
#ifndef DOWNSTREAM_DSTREAM_DISCARD__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_DISCARD__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_discard {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.discard_algo"; }

}  // namespace dstream_discard
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_DISCARD__GET_ALGO_NAME_HPP
