#pragma once
#ifndef DOWNSTREAM_AUXLIB_OVERFLOW_SHL_HPP
#define DOWNSTREAM_AUXLIB_OVERFLOW_SHL_HPP

#include <concepts>

#include "./DOWNSTREAM_CUDA_HD.hpp"

namespace downstream {
namespace _auxlib {

/**
 * Perform bitwise shift-left that may overflow without undefined behavior.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT>
DOWNSTREAM_CUDA_HD inline UINT overflow_shl(const UINT a, const UINT b) {
  return b < sizeof(UINT) * 8 ? a << b : 0;
}

}  // namespace _auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_OVERFLOW_SHL_HPP
