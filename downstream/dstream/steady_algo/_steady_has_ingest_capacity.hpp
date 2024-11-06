#ifndef STEADY_HAS_INGEST_CAPACITY_H
#define STEADY_HAS_INGEST_CAPACITY_H

#include <cassert>
#include "_steady_get_ingest_capacity.hpp"

bool steady_has_ingest_capacity(int64_t S, int64_t T) {
    assert(T >= 0);
    std::optional<int64_t> ingest_capacity = steady_get_ingest_capacity(S);
    return !ingest_capacity.has_value() || T < ingest_capacity.value();
}

#endif // STEADY_HAS_INGEST_CAPACITY_H