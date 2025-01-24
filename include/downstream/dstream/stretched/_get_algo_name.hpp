#pragma once
#ifndef DOWNSTREAM_DSTREAM_STRETCHED__GET_ALGO_NAME_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED__GET_ALGO_NAME_HPP

#include <string_view>

namespace downstream {
namespace dstream_stretched {

/**
 * Get dstream string identifier for algorithm.
 */
constexpr std::string_view get_algo_name() { return "dstream.stretched_algo"; }

}  // namespace dstream_stretched
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED__GET_ALGO_NAME_HPP
