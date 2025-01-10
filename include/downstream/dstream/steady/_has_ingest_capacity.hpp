#ifndef DOWNSTREAM_DSTREAM_STEADY_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STEADY_HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <cstdint>

namespace downstream {
namespace dstream_steady {

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
const bool has_ingest_capacity(const uint64_t S, const uint64_t T) {
  assert(T >= 0);
  return (std::popcount(S) == 1) and S > 1;
}

}  // namespace dstream_steady
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STEADY_HAS_INGEST_CAPACITY_HPP
