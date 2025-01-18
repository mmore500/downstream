#pragma once
#ifndef DOWNSTREAM_AUXLIB_MODPOW2_HPP
#define DOWNSTREAM_AUXLIB_MODPOW2_HPP

#include <bit>
#include <cassert>
#include <concepts>

namespace downstream {
namespace _auxlib {

/**
 * Perform fast mod using bitwise operations.
 *
 * @param x The dividend of the mod operation. Must be a positive integer.
 * @param n The divisor of the mod operation. Must be a positive integer and a
 * power of 2.
 * @returns The remainder of dividing the dividend by the divisor.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT>
inline UINT modpow2(const UINT x, const UINT n) {
  assert(std::has_single_bit(n));
  return x & (n - 1);
}

}  // namespace _auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_MODPOW2_HPP
