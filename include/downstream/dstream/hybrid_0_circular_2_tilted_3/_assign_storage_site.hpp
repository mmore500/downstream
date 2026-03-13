#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_2_TILTED_3__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_2_TILTED_3__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "../circular/_assign_storage_site.hpp"
#include "../tilted/_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_circular_2_tilted_3 {

/**
 * Internal implementation of site selection for hybrid circular/tilted
 * curation.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size. Must be divisible by 3, with S/3 being a power of two.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_hybrid_0_circular_2_tilted_3::has_ingest_capacity<UINT>(S, T));

  const UINT third_S = S / 3;
  const UINT two_thirds_S = 2 * third_S;
  const UINT remainder = T % 3;
  if (remainder < 2) {
    const UINT adj_T = (T / 3) * 2 + remainder;
    const UINT site =
        dstream_circular::_assign_storage_site<UINT>(two_thirds_S, adj_T);
    return (site == two_thirds_S) ? S : site;
  } else {
    const UINT adj_T = T / 3;
    const UINT site =
        dstream_tilted::_assign_storage_site<UINT>(third_S, adj_T);
    return (site == third_S) ? S : two_thirds_S + site;
  }
}

/**
 * Site selection algorithm for hybrid circular/tilted curation.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 * @param S Buffer size.
 *     Must be divisible by 3, with S/3 being a power of two.
 * @param T Current logical time.
 * @returns Selected site, if any.
 *     Returns nullopt if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site =
      dstream_hybrid_0_circular_2_tilted_3::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_hybrid_0_circular_2_tilted_3
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_CIRCULAR_2_TILTED_3__ASSIGN_STORAGE_SITE_HPP
