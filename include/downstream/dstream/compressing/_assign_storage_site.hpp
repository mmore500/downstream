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
 * Site selection for compressing curation with even buffer size.
 *
 * Site 0 is special (always holds T=0). Remaining S-1 sites are managed
 * with modulus M = S - 1.
 *
 * @param S Buffer size. Must be positive and even.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site_even_S(const UINT S, const UINT T) {
  assert((S & 1) == 0);
  constexpr UINT _1{1};
  namespace aux = downstream::_auxlib;

  if (T == 0) return 0;

  const UINT M = S - _1;
  const UINT T_ = T - _1;
  const UINT si = std::bit_width(
      static_cast<UINT>(T_ / M));  // Current sampling interval
  const UINT h =
      aux::countr_zero_casted<UINT>(std::max(T_, _1));  // Hanoi value
  if (h < si) [[likely]]
    return S;  // discard without storing
  else
    return T_ % M + _1;
}

/**
 * Site selection for compressing curation with odd buffer size.
 *
 * No special site. All S sites participate uniformly with modulus M = S.
 *
 * @param S Buffer size. Must be positive and odd.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site_odd_S(const UINT S, const UINT T) {
  assert((S & 1) == 1);
  constexpr UINT _1{1};
  namespace aux = downstream::_auxlib;

  const UINT M = S;
  const UINT si = std::bit_width(
      static_cast<UINT>(T / M));  // Current sampling interval
  const UINT h =
      aux::countr_zero_casted<UINT>(std::max(T, _1));  // Hanoi value
  if (h < si) [[likely]]
    return S;  // discard without storing
  else
    return T % M;
}

/**
 * Internal implementation of site selection for compressing curation.
 *
 * @param S Buffer size. Must be positive.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_compressing::has_ingest_capacity<UINT>(S, T));

  return (S & 1) == 0
    ? dstream_compressing::_assign_storage_site_even_S<UINT>(S, T)
    : dstream_compressing::_assign_storage_site_odd_S<UINT>(S, T);
}

/**
 * Site selection algorithm for compressing curation.
 *
 * @param S Buffer size. Must be positive.
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
