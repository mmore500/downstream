#pragma once
#ifndef DOWNSTREAM_AUXLIB_STD_BIT_HPP
#define DOWNSTREAM_AUXLIB_STD_BIT_HPP

#ifdef __CUDACC__
#include <cuda/std/bit>
#else
#include <bit>
#endif

namespace downstream {
namespace _auxlib {
namespace std_bit {

#ifdef __CUDACC__
namespace src = ::cuda::std;
#else
namespace src = ::std;
#endif

using src::bit_floor;
using src::bit_width;
using src::countr_zero;
using src::has_single_bit;
using src::popcount;

}  // namespace std_bit
}  // namespace _auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_STD_BIT_HPP
