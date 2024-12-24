#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_GET_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_GET_INGEST_CAPACITY_HPP

#include <bitset>
#include <cstdint>
#include <bit>
#include <optional>

namespace downstream {
namespace dstream {
namespace tilted_algo {

const uint64_t tilted_get_ingest_capacity(const uint64_t S) {
  return (uint64_t{1} << S) - 1;
}

} // namespace tilted_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_GET_INGEST_CAPACITY_HPP