#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP

#include "_tilted_get_ingest_capacity.hpp"
#include <bit>
#include <cassert>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace tilted_algo {

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

} // namespace tilted_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP