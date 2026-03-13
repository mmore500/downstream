#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_3_STEADY_4__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_3_STEADY_4__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../circular/_assign_storage_site.hpp"
#include "../steady/_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_circular_3_steady_4 {

/**
 * Internal implementation of site selection for hybrid circular/steady
 * curation.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size.
 *     Must be divisible by 4, with S/4 being a power of two.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_hybrid_0_circular_3_steady_4::has_ingest_capacity<UINT>(S, T));

  const UINT frac_S = S / 4;
  const UINT circ_S = 3 * frac_S;
  const UINT remainder = T % 4;
  if (remainder < 3) {
    const UINT adj_T = (T / 4) * 3 + remainder;
    const UINT site =
        dstream_circular::_assign_storage_site<UINT>(circ_S, adj_T);
    return (site == circ_S) ? S : site;
  } else {
    const UINT adj_T = T / 4;
    const UINT site =
        dstream_steady::_assign_storage_site<UINT>(frac_S, adj_T);
    return (site == frac_S) ? S : circ_S + site;
  }
}

/**
 * Site selection algorithm for hybrid circular/steady curation.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size.
 *     Must be divisible by 4, with S/4 being a power of two.
 * @param T Current logical time.
 * @returns Selected site, if any.
 *     Returns nullopt if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site =
      dstream_hybrid_0_circular_3_steady_4::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_hybrid_0_circular_3_steady_4
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_3_STEADY_4__ASSIGN_STORAGE_SITE_HPP
