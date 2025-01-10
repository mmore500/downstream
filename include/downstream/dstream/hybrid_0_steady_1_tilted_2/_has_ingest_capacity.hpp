#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2_HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <cstdint>
#include <optional>

#include "../steady/_has_ingest_capacity.hpp"
#include "../tilted/_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_steady_1_tilted_2 {

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
  const uint64_t half_S = S >> 1;
  const bool has_capacity_1st =
      dstream_steady::has_ingest_capacity(half_S, T >> 1);
  const bool has_capacity_2nd =
      ((T == 0) or dstream_tilted::has_ingest_capacity(half_S, (T - 1) >> 1));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace dstream_hybrid_0_steady_1_tilted_2
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2_HAS_INGEST_CAPACITY_HPP
