#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_TILTED_2_STEADY_3__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_TILTED_2_STEADY_3__HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../tilted/_has_ingest_capacity.hpp"
#include "../steady/_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_tilted_2_steady_3 {

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
  if (S < 3 or S % 3 != 0) {
    return false;
  }
  const UINT third_S = S / 3;
  const UINT two_thirds_S = 2 * third_S;
  const UINT T_div_3 = T / 3;
  const bool has_capacity_1st =
      dstream_tilted::has_ingest_capacity<UINT>(
          two_thirds_S, T_div_3 * 2 + static_cast<UINT>(T % 3 > 0));
  const bool has_capacity_2nd =
      ((T < 2) or
       dstream_steady::has_ingest_capacity<UINT>(third_S, (T - 2) / 3));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace dstream_hybrid_0_tilted_2_steady_3
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_TILTED_2_STEADY_3__HAS_INGEST_CAPACITY_HPP
