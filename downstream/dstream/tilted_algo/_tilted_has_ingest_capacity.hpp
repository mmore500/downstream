#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP

#include <cassert>
#include <cstdint>
#include <optional>
#include <bit>

namespace downstream {
namespace dstream {
namespace tilted_algo {

bool tilted_has_ingest_capacity(uint64_t S, uint64_t T) {
    assert(T >= 0);
    bool surface_size_ok = std::popcount(S) == 1 && S > 1;

    if (!surface_size_ok) {
        return false;
    }

    if (S >= 64) {
        return true;
    }

    uint64_t ingest_capacity = (uint64_t{1} << S) - 1;
    return T < ingest_capacity;
}

}  // namespace tilted_algo
}  // namespace dstream
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_HAS_INGEST_CAPACITY_HPP