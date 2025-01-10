#pragma once
#ifndef DOWNSTREAM_DSTREAM_TILTED_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED_HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <cstdint>

namespace downstream {
namespace dstream_tilted {

/**
 * Does this algorithm have the capacity to ingest a data item at logical time
 * T?
 *
 * @param S The number of buffer sites available.
 * @param T Current logical time.
 * @returns Whether there is capacity to ingest at time T.
 *
 * @exceptsafe no-throw
 */
const bool has_ingest_capacity(const uint64_t S, const uint64_t T) {
  const bool surface_size_ok = S > 1 and (std::popcount(S) == 1);
  if (!surface_size_ok) return false;
  if (S >= 8 * sizeof(uint64_t)) return true;

  const uint64_t ingest_capacity = (uint64_t{1} << S) - 1;
  return T < ingest_capacity;
}

}  // namespace dstream_tilted
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED_HAS_INGEST_CAPACITY_HPP
