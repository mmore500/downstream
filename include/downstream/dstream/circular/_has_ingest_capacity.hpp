#pragma once
#ifndef DOWNSTREAM_DSTREAM_CIRCULAR__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_CIRCULAR__HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <concepts>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"

namespace downstream {
namespace dstream_circular {

/**
 * Does this algorithm have the capacity to ingest a data item at logical time
 * T?
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S The number of buffer sites available.
 * @param T Queried logical time.
 * @returns Whether there is capacity to ingest at time T.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
bool has_ingest_capacity(const UINT S, const UINT T) {
  assert(T >= 0);
  return std::has_single_bit(S) and S > 1;
}

}  // namespace dstream_circular
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_CIRCULAR__HAS_INGEST_CAPACITY_HPP
