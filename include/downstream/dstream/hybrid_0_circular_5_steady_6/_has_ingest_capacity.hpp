#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_5_STEADY_6__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_5_STEADY_6__HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../circular/_has_ingest_capacity.hpp"
#include "../steady/_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_circular_5_steady_6 {

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
  if (S < 6 or S % 6 != 0) {
    return false;
  }
  const UINT frac_S = S / 6;
  const UINT circ_S = 5 * frac_S;
  const UINT T_div_N = T / 6;
  const UINT T_mod_N = T % 6;
  const UINT adj_T_mod =
      (T_mod_N < 5) ? T_mod_N : static_cast<UINT>(5 - 1);
  const bool has_capacity_1st =
      dstream_circular::has_ingest_capacity<UINT>(
          circ_S, T_div_N * 5 + adj_T_mod);
  const bool has_capacity_2nd =
      ((T < 5) or
       dstream_steady::has_ingest_capacity<UINT>(frac_S, (T - 5) / 6));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace dstream_hybrid_0_circular_5_steady_6
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_5_STEADY_6__HAS_INGEST_CAPACITY_HPP
