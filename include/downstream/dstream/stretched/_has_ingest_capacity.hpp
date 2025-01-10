#pragma once
#ifndef DOWNSTREAM_DSTREAM_STRETCHED__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED__HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <concepts>

#include "../../auxlib/DOWNSTREAM_UINT.hpp"

namespace downstream {
namespace dstream_stretched {

/**
 * Does this algorithm have the capacity to ingest a data item at logical time
 * T?
 *
 * @param S The number of buffer sites available.
 * @param T Queried logical time.
 * @returns Whether there is capacity to ingest at time T.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
const bool has_ingest_capacity(const UINT S, const UINT T) {
  const bool surface_size_ok = S > 1 and (std::popcount(S) == 1);
  if (!surface_size_ok) return false;
  if (S >= 8 * sizeof(UINT)) return true;

  const UINT ingest_capacity = (UINT{1} << S) - 1;
  return T < ingest_capacity;
}

}  // namespace dstream_stretched
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED__HAS_INGEST_CAPACITY_HPP
