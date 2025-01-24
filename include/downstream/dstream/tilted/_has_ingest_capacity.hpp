#pragma once
#ifndef DOWNSTREAM_DSTREAM_TILTED__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED__HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <concepts>
#include <limits>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../../_auxlib/overflow_shr.hpp"

namespace downstream {
namespace dstream_tilted {

/**
 * Does this algorithm have the capacity to ingest a data item at logical time
 * T?
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S The number of buffer sites available.
 * @param T Current logical time.
 * @returns Whether there is capacity to ingest at time T.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
bool has_ingest_capacity(const UINT S, const UINT T) {
  const bool surface_size_ok = S > 1 and std::has_single_bit(S);
  const UINT overflow_epsilon = T == std::numeric_limits<UINT>::max();
  return surface_size_ok and
         0 == downstream::_auxlib::overflow_shr<UINT>(              //
                  (T - overflow_epsilon) + 1, S - overflow_epsilon  //
              );
}

}  // namespace dstream_tilted
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED__HAS_INGEST_CAPACITY_HPP
