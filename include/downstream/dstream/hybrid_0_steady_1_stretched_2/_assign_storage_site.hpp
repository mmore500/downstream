#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <cassert>
#include <cstdint>
#include <optional>

#include "../steady/_assign_storage_site.hpp"
#include "../stretched/_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_steady_1_stretched_2 {

/**
 * Internal implementation of site selection algorithm for hybrid curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time.
 * @returns The selected storage site, or S if no site should be selected.
 *
 * @exceptsafe no-throw
 */
const uint64_t _assign_storage_site(const uint64_t S, const uint64_t T) {
  assert(dstream_hybrid_0_steady_1_stretched_2::has_ingest_capacity(S, T));

  const uint64_t half_S = S >> 1;
  const uint64_t half_T = T >> 1;
  if ((T & 1) == 0) {
    const uint64_t site = dstream_steady::_assign_storage_site(half_S, half_T);
    return (site == half_S) ? S : site;
  } else {
    return half_S + dstream_stretched::_assign_storage_site(half_S, half_T);
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
const std::optional<uint64_t> assign_storage_site(const uint64_t S,
                                                  const uint64_t T) {
  const uint64_t site =
      dstream_hybrid_0_steady_1_stretched_2::_assign_storage_site(S, T);
  return site == S ? std::nullopt : std::optional<uint64_t>(site);
}

}  // namespace dstream_hybrid_0_steady_1_stretched_2
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2__ASSIGN_STORAGE_SITE_HPP
