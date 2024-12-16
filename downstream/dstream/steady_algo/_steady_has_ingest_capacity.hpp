#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_HAS_INGEST_CAPACITY_HPP

#include "_steady_get_ingest_capacity.hpp"
#include <cassert>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

const bool steady_has_ingest_capacity(const uint64_t S, const uint64_t T) {
  assert(T >= 0);
  const std::optional<uint64_t> ingest_capacity = steady_get_ingest_capacity(S);
  return !ingest_capacity.has_value() || T < ingest_capacity.value();
}

} // namespace steady_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_HAS_INGEST_CAPACITY_HPP