#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <bit>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

/**
 * Internal implementation of site selection algorithm for steady curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time.
 * @returns The selected storage site, or S if no site should be selected.
 *
 * @exceptsafe no-throw
 */
const uint64_t _steady_assign_storage_site(const uint64_t S, const uint64_t T) {
  const uint64_t s = std::bit_width(S) - 1;
  const uint64_t blT = std::bit_width(T);
  const uint64_t t = blT - std::min(s, blT);   // Current epoch
  const uint64_t h = std::countr_zero(T + 1);  // Current hanoi value
  if (h < t) {  // If not a top n(T) hanoi value...
    return S;   // ...discard without storing
  }
  const uint64_t i = T >> (h + 1);  // Hanoi value incidence (i.e., num seen)
  uint64_t k_b, o, w;  // Bunch position, within-bunch offset, segment width
  if (i == 0) {        // Special case the 0th bunch
    k_b = 0;           // Bunch position
    o = 0;             // Within-bunch offset
    w = s + 1;         // Segment width
  } else {
    const uint64_t j = std::bit_floor(i) - 1;  // Num full-bunch segments
    const uint64_t B = std::bit_width(j);      // Num full bunches
    k_b = (1 << B) * (s - B + 1);              // Bunch position
    // substituting t = s - blT into h + 1 - t
    w = h + s + 1 - blT;                             // Segment width
    if (w <= 0) {
      return S;
    }
    o = w * (i - j - 1);  // Within-bunch offset
  }
  const uint64_t p = h % w;  // Within-segment offset
  return k_b + o + p;        // Calculate placement site
}

/**
 * Site selection algorithm for steady curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time.
 * @returns Selected site, if any. Returns nullopt if no site should be
 * selected.
 *
 * @exceptsafe no-throw
 */
const std::optional<uint64_t> steady_assign_storage_site(const uint64_t S,
                                                         const uint64_t T) {
  const uint64_t site = _steady_assign_storage_site(S, T);
  return site == S ? std::nullopt : std::optional<uint64_t>(site);
}

}  // namespace steady_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP
