#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP

#include <bit>
#include <bitset>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace stretched_algo {

/**
 * How many data item ingestions does this algorithm support?
 *
 * @param S Surface size parameter
 * @returns (2^S - 1) if surface size is valid (power of 2 greater than 1),
 *     0 otherwise.
 *
 * @see stretched_algo::has_ingest_capacity Does this algorithm have the
 * capacity to ingest n data items?
 *
 * @exceptsafe no-throw
 */
const uint64_t stretched_get_ingest_capacity(const uint64_t S) {
  return (uint64_t{1} << S) - 1;
}

}  // namespace stretched_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP
