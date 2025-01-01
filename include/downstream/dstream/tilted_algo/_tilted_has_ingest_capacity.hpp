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
#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <cstdint>
#include <optional>

#include "_tilted_get_ingest_capacity.hpp"

namespace downstream {
namespace dstream {
namespace tilted_algo {

/**
* Does this algorithm have the capacity to ingest a data item at logical time T?
*
* @param S The number of buffer sites available.
* @param T Current logical time.
* @returns Whether there is capacity to ingest at time T.
*
* @see tilted_algo::get_ingest_capacity How many data item ingestions does this algorithm support?
*
* @exceptsafe no-throw
*/
const bool tilted_has_ingest_capacity(const uint64_t S, const uint64_t T) {
  assert(T >= 0);
  const bool surface_size_ok = std::has_single_bit(S) && S > 1;

  if (!surface_size_ok) {
    return false;
  }

  if (S >= 64) {
    return true;
  }

  const uint64_t ingest_capacity = tilted_get_ingest_capacity(S);
  return T < ingest_capacity;
}

}  // namespace tilted_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP