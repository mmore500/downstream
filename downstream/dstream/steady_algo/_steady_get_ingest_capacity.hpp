#ifndef STEADY_INGEST_CAPACITY_H
#define STEADY_INGEST_CAPACITY_H

#include <bitset>
#include <optional>

namespace downstream {
namespace dstream {
namespace steady_algo {

std::optional<uint64_t> steady_get_ingest_capacity(uint64_t S) {
  bool surface_size_ok = std::has_single_bit(S) && S > 1;
  return surface_size_ok ? std::nullopt : std::optional<uint64_t>(0);
}

} // namespace steady_algo
} // namespace dstream
} // namespace downstream

#endif // STEADY_INGEST_CAPACITY_H