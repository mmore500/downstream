#pragma once
#ifndef DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP
#define DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP

#include <bit>
#include <concepts>

namespace downstream {
namespace _auxlib {

template <std::unsigned_integral UINT>
inline UINT bit_floor_casted(const UINT v) {
  return static_cast<UINT>(std::bit_floor(v));
}

template <std::unsigned_integral UINT>
inline UINT bit_width_casted(const UINT v) {
  return static_cast<UINT>(std::bit_width(v));
}

template <std::unsigned_integral UINT>
inline UINT countr_zero_casted(const UINT v) {
  return static_cast<UINT>(std::countr_zero(v));
}

template <std::unsigned_integral UINT>
inline UINT popcount_casted(const UINT v) {
  return static_cast<UINT>(std::popcount(v));
}

}  // namespace _auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP
