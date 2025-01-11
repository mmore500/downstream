#pragma once
#ifndef DOWNSTREAM_DSTREAM_STRETCHED__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <bit>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../auxlib/DOWNSTREAM_UINT.hpp"
#include "../../auxlib/overflow_shr.hpp"
#include "../../auxlib/std_bit_casted.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_stretched {

/**
 * Internal implementation of site selection for stretched curation.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size.
 *      Must be a power of two greater than 1, and 2 * S must not overflow UINT.
 * @param T Current logical time.
 *      Must be less than 2^S - 1.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_stretched::has_ingest_capacity<UINT>(S, T));
  assert(2 * S > S);  // otherwise, calculations overflow

  constexpr UINT _1{1};
  namespace aux = downstream::auxlib;

  const UINT s = std::bit_width(S) - _1;
  const UINT blT = std::bit_width(T);
  const UINT t = blT - std::min(s, blT);                 // Current epoch
  const UINT h = aux::countr_zero_casted<UINT>(T + _1);  // Current hanoi value
  const UINT i = aux::overflow_shr<UINT>(T, h + _1);
  // ^^^ Hanoi value incidence (i.e., num seen)

  const UINT blt = std::bit_width(t);  // Bit length of t
  bool epsilon_tau =
      aux::bit_floor_casted<UINT>(t << _1) > t + blt;  // Correction factor
  const UINT tau = blt - epsilon_tau;                  // Current meta-epoch
  const UINT b = std::max<UINT>(S >> (tau + _1), _1);
  // ^^^ Num bunches available to h.v.
  if (i >= b) {  // If seen more than sites reserved to hanoi value...
    return S;    // ... discard without storing
  }

  const UINT b_l = i;  // Logical bunch index...
  // ... i.e., in order filled (increasing nestedness/decreasing init size r)

  // Need to calculate physical bunch index...
  // ... i.e., position among bunches left-to-right in buffer space
  const UINT v =
      std::bit_width(b_l);  // Nestedness depth level of physical bunch
  const UINT w =
      (S >> v) * (v != 0);  // Num bunches spaced between bunches in nest level
  const UINT o = w >> _1;  // Offset of nestedness level in physical bunch order
  const UINT p =
      b_l - std::bit_floor(b_l);  // Bunch position within nestedness level
  const UINT b_p = o + w * p;     // Physical bunch index...
  // ... i.e., in left-to-right sequential bunch order

  // Need to calculate buffer position of b_p'th bunch
  const bool epsilon_k_b = (b_l != 0);  // Correction factor for zeroth bunch...
  // ... i.e., bunch r=s at site k=0
  const UINT k_b = (b_p << 1) + aux::popcount_casted<UINT>((S << 1) - b_p) - 1 -
                   epsilon_k_b;  // Site index of bunch

  return k_b + h;  // Calculate placement site...
                   // ... where h.v. h is offset within bunch
}

/**
 * Site selection algorithm for stretched curation.
 *
 * What buffer site should the T'th data item be stored to?
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size.
 *      Must be a power of two greater than 1, and 2 * S must not overflow UINT.
 * @param T Current logical time.
 *      Must be less than 2^S - 1.
 * @returns Selected site, if any.
 *     Returns nullopt if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site = dstream_stretched::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_stretched
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED__ASSIGN_STORAGE_SITE_HPP
