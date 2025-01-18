#pragma once
#ifndef DOWNSTREAM_DSTREAM_TILTED__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_TILTED__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_tilted {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.tilted_algo"; }

}  // namespace dstream_tilted
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED__GET_ALGO_NAME_HPP
