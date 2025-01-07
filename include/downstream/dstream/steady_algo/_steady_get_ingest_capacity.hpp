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
 * @see steady_algo::has_ingest_capacity Does this algorithm have the capacity
 * to ingest n data items?
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
