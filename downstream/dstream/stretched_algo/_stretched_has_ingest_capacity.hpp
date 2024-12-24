#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_HAS_INGEST_CAPACITY_HPP

#include <bit>
#include <cassert>
#include <cstdint>
#include <optional>

#include "_stretched_get_ingest_capacity.hpp"

namespace downstream {
namespace dstream {
namespace stretched_algo {

const bool stretched_has_ingest_capacity(const uint64_t S, const uint64_t T) {
  assert(T >= 0);
  const bool surface_size_ok = std::has_single_bit(S) && S > 1;

  if (!surface_size_ok) {
    return false;
  }

  if (S >= 64) {
    return true;
  }

  const uint64_t ingest_capacity = stretched_get_ingest_capacity(S);
  return T < ingest_capacity;
}

}  // namespace stretched_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_HAS_INGEST_CAPACITY_HPP