#pragma once
#ifndef DOWNSTREAM_DSTREAM_COMPRESSING__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_COMPRESSING__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <bit>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../../_auxlib/overflow_shl.hpp"
#include "../../_auxlib/overflow_shr.hpp"
#include "../../_auxlib/std_bit_casted.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_compressing {

/**
 * Internal implementation of site selection for compressing curation.
 *
 * @param S Buffer size.
 *      Must be a power of two greater than 1.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_compressing::has_ingest_capacity<UINT>(S, T));

  constexpr UINT _1{1};
  namespace aux = downstream::_auxlib;

  // special-case site 0 for T = 0, to fill entire buffer
  if (T == 0) return 0;

  const UINT T_ = T - _1;
  const UINT si = std::bit_width(
      static_cast<UINT>(T_ / (S - _1)));  // Current sampling interval
  const UINT h =
      aux::countr_zero_casted<UINT>(std::max(T_, _1));  // Current hanoi value
  if (h < si) [[likely]]
    return S;  // discard without storing
  else
    return T_ % (S - _1) + _1;
}

/**
 * Site selection algorithm for compressing curation.
 *
 * @param S Buffer size.
 *      Must be a power of two greater than 1.
 * @param T Current logical time.
 * @returns Selected site, if any.
 *     Returns nullopt if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site = dstream_compressing::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_compressing
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_COMPRESSING__ASSIGN_STORAGE_SITE_HPP
