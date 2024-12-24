#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP

#include <bit>
#include <bitset>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace stretched_algo {

const uint64_t stretched_get_ingest_capacity(const uint64_t S) {
  return (uint64_t{1} << S) - 1;
}

}  // namespace stretched_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_GET_INGEST_CAPACITY_HPP