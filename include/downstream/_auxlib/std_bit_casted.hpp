#pragma once
#ifndef DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP
#define DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP

#include <concepts>

#include "./DOWNSTREAM_CUDA_HD.hpp"
#include "./std_bit.hpp"

namespace downstream {
namespace _auxlib {

template <std::unsigned_integral UINT>
DOWNSTREAM_CUDA_HD
inline UINT bit_floor_casted(const UINT v) {
  return static_cast<UINT>(std_bit::bit_floor(v));
}

template <std::unsigned_integral UINT>
DOWNSTREAM_CUDA_HD
inline UINT bit_width_casted(const UINT v) {
  return static_cast<UINT>(std_bit::bit_width(v));
}

template <std::unsigned_integral UINT>
DOWNSTREAM_CUDA_HD
inline UINT countr_zero_casted(const UINT v) {
  return static_cast<UINT>(std_bit::countr_zero(v));
}

template <std::unsigned_integral UINT>
DOWNSTREAM_CUDA_HD
inline UINT popcount_casted(const UINT v) {
  return static_cast<UINT>(std_bit::popcount(v));
}

}  // namespace _auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_STD_BIT_CASTED_HPP
