#pragma once
#ifndef DOWNSTREAM_DSTREAM_DISCARD__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_DISCARD__ASSIGN_STORAGE_SITE_HPP

#include <cassert>
#include <concepts>
#include <optional>

#include "../../_auxlib/DOWNSTREAM_CUDA_HD.hpp"
#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_discard {

/**
 * Internal implementation of site selection for discard curation.
 *
 * @param S Buffer size. Must be non-negative.
 * @param T Current logical time.
 * @returns The selected storage site, if any.
 *     Returns S if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
DOWNSTREAM_CUDA_HD UINT _assign_storage_site(const UINT S, const UINT T) {
  assert(dstream_discard::has_ingest_capacity<UINT>(S, T));

  return S;
}

/**
 * Site selection algorithm for discard curation.
 *
 * @param S Buffer size. Must be non-negative.
 * @param T Current logical time.
 * @returns Selected site, if any.
 *     Returns nullopt if no site should be selected (i.e., discard).
 *
 * @exceptsafe no-throw
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T) {
  const UINT site = dstream_discard::_assign_storage_site<UINT>(S, T);
  return site == S ? std::nullopt : std::optional<UINT>(site);
}

}  // namespace dstream_discard
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_DISCARD__ASSIGN_STORAGE_SITE_HPP
