#pragma once
#ifndef DOWNSTREAM_DSTREAM_STICKY__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STICKY__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_sticky {

/**
 * Internal implementation of site selection for sticky curation.
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
  assert(dstream_sticky::has_ingest_capacity<UINT>(S, T));

  return std::min(T, S);
}

/**
 * Site selection algorithm for sticky curation.
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
  const UINT site = dstream_sticky::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_sticky
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STICKY__ASSIGN_STORAGE_SITE_HPP
