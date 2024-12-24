#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP

#include <bitset>
#include <cstdint>
#include <bit>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

const uint64_t _steady_get_ingest_capacity(const uint64_t S) {
  const bool surface_size_ok = std::has_single_bit(S) && S > 1;
  return surface_size_ok ? S : 0;
}

const std::optional<uint64_t> steady_get_ingest_capacity(const uint64_t S) {
  const uint64_t ingest_capacity = _steady_get_ingest_capacity(S);
  return ingest_capacity == S ? std::nullopt : std::optional<uint64_t>(ingest_capacity);
}



} // namespace steady_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_GET_INGEST_CAPACITY_HPP