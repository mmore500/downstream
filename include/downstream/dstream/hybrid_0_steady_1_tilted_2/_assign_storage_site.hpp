#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../auxlib/DOWNSTREAM_UINT.hpp"
#include "../steady/_assign_storage_site.hpp"
#include "../tilted/_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_steady_1_tilted_2 {

/**
 * Internal implementation of site selection algorithm for hybrid curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time.
 * @returns The selected storage site, or S if no site should be selected.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
const UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_hybrid_0_steady_1_tilted_2::has_ingest_capacity<UINT>(S, T));

  const UINT half_S = S >> 1;
  const UINT half_T = T >> 1;
  if ((T & 1) == 0) {
    const UINT site =
        dstream_steady::_assign_storage_site<UINT>(half_S, half_T);
    return (site == half_S) ? S : site;
  } else {
    return half_S + dstream_tilted::_assign_storage_site<UINT>(half_S, half_T);
  }
}

/**
 * Site selection algorithm for hybrid curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time.
 * @returns Selected site, if any. Returns nullopt if no site should be
 * selected.
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
const std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site =
      dstream_hybrid_0_steady_1_tilted_2::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_hybrid_0_steady_1_tilted_2
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_TILTED_2__ASSIGN_STORAGE_SITE_HPP
