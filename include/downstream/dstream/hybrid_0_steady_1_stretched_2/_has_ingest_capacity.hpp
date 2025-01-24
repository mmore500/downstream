#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../steady/_has_ingest_capacity.hpp"
#include "../stretched/_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_steady_1_stretched_2 {

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
  const UINT half_S = S >> 1;
  const bool has_capacity_1st =
      dstream_steady::has_ingest_capacity<UINT>(half_S, T >> 1);
  const bool has_capacity_2nd =
      ((T == 0) or
       dstream_stretched::has_ingest_capacity<UINT>(half_S, (T - 1) >> 1));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace dstream_hybrid_0_steady_1_stretched_2
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__HAS_INGEST_CAPACITY_HPP
