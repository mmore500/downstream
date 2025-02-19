#pragma once
#ifndef DOWNSTREAM_DSTREAM_COMPRESSING__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_COMPRESSING__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_compressing {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() {
  return "dstream.compressing_algo";
}

}  // namespace dstream_compressing
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_COMPRESSING__GET_ALGO_NAME_HPP
