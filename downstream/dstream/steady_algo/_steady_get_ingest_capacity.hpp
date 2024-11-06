#ifndef STEADY_INGEST_CAPACITY_H
#define STEADY_INGEST_CAPACITY_H

#include <optional>
#include <bitset>

std::optional<int64_t> steady_get_ingest_capacity(int64_t S) {
    bool surface_size_ok = (S & (S - 1)) == 0 && S > 1;
    return surface_size_ok ? std::nullopt : std::optional<int64_t>(0);
}

#endif // STEADY_INGEST_CAPACITY_H