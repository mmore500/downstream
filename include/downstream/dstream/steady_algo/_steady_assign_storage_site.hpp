// -*- lsst-c++ -*-
/*
 * This file is part of downstream.
 *
 * Developed for the LSST Data Management System.
 * This product includes software developed by the LSST Project
 * (https://www.lsst.org).
 * See the COPYRIGHT file at the top-level directory of this distribution
 * for details of code ownership.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP

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
  const int64_t t = std::bit_width(T) - s;    // Current epoch (or negative)
  const int64_t h = std::countr_zero(T + 1);  // Current hanoi value
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
    w = h - t + 1;                             // Segment width
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
