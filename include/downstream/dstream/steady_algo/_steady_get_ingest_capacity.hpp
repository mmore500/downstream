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

#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP

#include <bit>
#include <bitset>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

/**
 * How many data item ingestions does this algorithm support?
 *
 * @param S Surface size parameter
 * @returns S if algorithm can ingest data items, 0 if invalid surface size.
 *     Returns S if the number of supported ingestions is unlimited.
 *
 * @see steady_algo::has_ingest_capacity Does this algorithm have the capacity to ingest n data items?
 *
 * @exceptsafe no-throw
 */
const uint64_t steady_get_ingest_capacity(const uint64_t S) {
  const bool surface_size_ok = std::has_single_bit(S) && S > 1;
  return surface_size_ok ? S : 0;
}

}  // namespace steady_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP