#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_11_STEADY_12__HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_11_STEADY_12__HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../circular/_has_ingest_capacity.hpp"
#include "../steady/_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_circular_11_steady_12 {

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
  if (S < 12 or S % 12 != 0) {
    return false;
  }
  const UINT frac_S = S / 12;
  const UINT circ_S = 11 * frac_S;
  const UINT T_div_N = T / 12;
  const UINT T_mod_N = T % 12;
  const UINT adj_T_mod =
      (T_mod_N < 11) ? T_mod_N : static_cast<UINT>(11 - 1);
  const bool has_capacity_1st =
      dstream_circular::has_ingest_capacity<UINT>(
          circ_S, T_div_N * 11 + adj_T_mod);
  const bool has_capacity_2nd =
      ((T < 11) or
       dstream_steady::has_ingest_capacity<UINT>(frac_S, (T - 11) / 12));
  return has_capacity_1st and has_capacity_2nd;
}

}  // namespace dstream_hybrid_0_circular_11_steady_12
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_11_STEADY_12__HAS_INGEST_CAPACITY_HPP
