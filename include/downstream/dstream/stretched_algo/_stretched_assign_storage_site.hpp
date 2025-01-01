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

#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <bit>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace stretched_algo {

/**
 * Internal implementation of site selection algorithm for stretched curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time. Must be less than 2^S - 1.
 * @returns The selected storage site, or S if no site should be selected.
 *
 * @exceptsafe no-throw
 */
const uint64_t _stretched_assign_storage_site(const uint64_t S,
                                              const uint64_t T) {
  const uint64_t s = std::bit_width(S) - 1;
  const uint64_t t =
      std::max(std::bit_width(T) - s, uint64_t{0});  // Current epoch
  const uint64_t h = std::countr_zero(T + 1);        // Current hanoi value
  const uint64_t i =
      (h + 1) >= 64 ? 0
                    : (T >> (h + 1));  // Hanoi value incidence (i.e., num seen)

  const uint64_t blt = std::bit_width(t);  // Bit length of t
  const uint64_t t_floor = t <= 0 ? 0 : 1 << (std::bit_width(t) - 1);
  const bool epsilon_tau = t_floor << 1 > t + blt;  // Correction factor
  const uint64_t tau = blt - epsilon_tau;           // Current meta-epoch
  const uint64_t b =
      (S >> (tau + 1)) ? (S >> (tau + 1)) : 1;  // Num bunches available to h.v.
  if (i >= b) {  // If seen more than sites reserved to hanoi value...
    return S;    // ... discard without storing
  }

  const uint64_t b_l = i;  // Logical bunch index...
  // ... i.e., in order filled (increasing nestedness/decreasing init size r)

  // Need to calculate physical bunch index...
  // ... i.e., position among bunches left-to-right in buffer space
  const uint64_t v =
      std::bit_width(b_l);  // Nestedness depth level of physical bunch
  const uint64_t w =
      (S >> v) * (v != 0);  // Num bunches spaced between bunches in nest level
  const uint64_t o =
      w >> 1;  // Offset of nestedness level in physical bunch order
  const uint64_t b_l_floor = b_l <= 0 ? 0 : 1 << (std::bit_width(b_l) - 1);
  const uint64_t p = b_l - b_l_floor;  // Bunch position within nestedness level
  const uint64_t b_p = o + w * p;      // Physical bunch index...
  // ... i.e., in left-to-right sequential bunch order

  // Need to calculate buffer position of b_p'th bunch
  const bool epsilon_k_b = (b_l != 0);  // Correction factor for zeroth bunch...
  // ... i.e., bunch r=s at site k=0
  const uint64_t k_b = (b_p << 1) + std::popcount((S << 1) - b_p) - 1 -
                       epsilon_k_b;  // Site index of bunch

  return k_b + h;  // Calculate placement site...
                   // ... where h.v. h is offset within bunch
}

/**
 * Site selection algorithm for stretched curation.
 *
 * @param S Buffer size. Must be a power of two.
 * @param T Current logical time. Must be less than 2^S - 1.
 * @returns Selected site, if any. Returns nullopt if no site should be selected.
 *
 * @exceptsafe no-throw
 */
const std::optional<uint64_t> stretched_assign_storage_site(const uint64_t S,
                                                            const uint64_t T) {
  const uint64_t site = _stretched_assign_storage_site(S, T);
  return site == S ? std::nullopt : std::optional<uint64_t>(site);
}

}  // namespace stretched_algo
}  // namespace dstream
}  // namespace downstream
#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP