#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP

#include <cstdint>
#include <optional>
#include <bit>

namespace downstream {
namespace dstream {
namespace steady_algo {

constexpr int64_t bit_floor(int64_t x) {
    if (x <= 0) return 0;
    return int64_t{1} << (std::bit_width(static_cast<uint64_t>(x)) - 1);
}

constexpr int ctz(int64_t x) {
    if (x == 0) return 0;
    return std::countr_zero(static_cast<uint64_t>(x));
}

std::optional<int64_t> steady_assign_storage_site(int64_t S, int64_t T) {
    int s = std::bit_width(static_cast<uint64_t>(S)) - 1;
    int t = std::bit_width(static_cast<uint64_t>(T)) - s;  // Current epoch (or negative)
    int h = ctz(T + 1);  // Current hanoi value
    if (h < t) {  // If not a top n(T) hanoi value...
        return std::nullopt;  // ...discard without storing
    }
    int64_t i = T >> (h + 1);  // Hanoi value incidence (i.e., num seen)
    if (i == 0) {  // Special case the 0th bunch
        int64_t k_b = 0;  // Bunch position
        int64_t o = 0;    // Within-bunch offset
        int64_t w = s + 1;  // Segment width
    } else {
        int64_t j = bit_floor(i) - 1;  // Num full-bunch segments
        int B = std::bit_width(static_cast<uint64_t>(j));  // Num full bunches
        int64_t k_b = (int64_t{1} << B) * (s - B + 1);  // Bunch position
        int64_t w = h - t + 1;  // Segment width
        if (w <= 0) {
            return std::nullopt;
        }
        int64_t o = w * (i - j - 1);  // Within-bunch offset
        int64_t p = h % w;  // Within-segment offset
        return k_b + o + p;  // Calculate placement site
    }
    return 0;
}

} // namespace steady_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_STEADY_ALGO_STEADY_ASSIGN_STORAGE_SITE_HPP