#ifndef STEADY_HAS_INGEST_CAPACITY_H
#define STEADY_HAS_INGEST_CAPACITY_H

#include "_steady_get_ingest_capacity.hpp"
#include <cassert>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

bool steady_has_ingest_capacity(uint64_t S, uint64_t T) {
  assert(T >= 0);
  std::optional<uint64_t> ingest_capacity = steady_get_ingest_capacity(S);
  return !ingest_capacity.has_value() || T < ingest_capacity.value();
}

} // namespace steady_algo
} // namespace dstream
} // namespace downstream

#endif // STEADY_HAS_INGEST_CAPACITY_H