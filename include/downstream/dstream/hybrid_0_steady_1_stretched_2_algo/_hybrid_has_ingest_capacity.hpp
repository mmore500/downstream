#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HYBRID_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HYBRID_HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <cstdint>
#include <optional>

#include "../steady_algo/_steady_has_ingest_capacity.hpp"
#include "../stretched_algo/_stretched_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream {
namespace hybrid_0_steady_1_stretched_2_algo {

/**
 * Does this algorithm have the capacity to ingest a data item at logical time
 * T?
 *
 * @param S The number of buffer sites available.
 * @param T Queried logical time.
 * @returns Whether there is capacity to ingest at time T.
 *
 * @see steady_get_ingest_capacity How many data item ingestions does this
 * algorithm support?
 *
 * @exceptsafe no-throw
 */
const bool hybrid_has_ingest_capacity(const uint64_t S, const uint64_t T) {
  const uint64_t half_S = S >> 1;
  const bool has_capacity_1st =
      steady_algo::steady_has_ingest_capacity(half_S, T >> 1);
  const bool has_capacity_2nd =
      ((T == 0) or
       stretched_algo::stretched_has_ingest_capacity(half_S, (T - 1) >> 1));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace hybrid_0_steady_1_stretched_2_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HYBRID_HAS_INGEST_CAPACITY_HPP
