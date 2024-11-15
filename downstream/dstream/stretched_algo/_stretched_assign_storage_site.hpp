#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP
#include <bit>
#include <cstdint>
#include <optional>
#include <algorithm>

namespace downstream {
namespace dstream {
namespace stretched_algo {

std::optional<uint64_t>  stretched_assign_storage_site(uint64_t S, uint64_t T) {
    uint64_t s = std::bit_width(S) - 1;
    uint64_t t = std::max(std::bit_width(T) - s, uint64_t{0});  // Current epoch
    uint64_t h = std::countr_zero(T + 1);  // Current hanoi value
    uint64_t i = T >> (h + 1);  // Hanoi value incidence (i.e., num seen)

    uint64_t blt = std::bit_width(t);  // Bit length of t
    uint64_t t_floor = t <= 0 ? 0 : 1 << (std::bit_width(t) - 1);
    bool epsilon_tau = t_floor << 1 > t + blt;  // Correction factor
    uint64_t tau = blt - epsilon_tau;  // Current meta-epoch
    uint64_t b = (S >> (tau + 1)) ? (S >> (tau + 1)) : 1;  // Num bunches available to h.v.
    if (i >= b) {  // If seen more than sites reserved to hanoi value...
        return std::nullopt;  // ... discard without storing
    }

    uint64_t b_l = i;  // Logical bunch index...
    // ... i.e., in order filled (increasing nestedness/decreasing init size r)

    // Need to calculate physical bunch index...
    // ... i.e., position among bunches left-to-right in buffer space
    uint64_t v = std::bit_width(b_l);  // Nestedness depth level of physical bunch
    uint64_t w = (S >> v) * (v != 0);  // Num bunches spaced between bunches in nest level
    uint64_t o = w >> 1;  // Offset of nestedness level in physical bunch order
    uint64_t b_l_floor = b_l <= 0 ? 0 : 1 << (std::bit_width(b_l) - 1);
    uint64_t p = b_l - b_l_floor;  // Bunch position within nestedness level
    uint64_t b_p = o + w * p;  // Physical bunch index...
    // ... i.e., in left-to-right sequential bunch order

    // Need to calculate buffer position of b_p'th bunch
    bool epsilon_k_b = (b_l != 0);  // Correction factor for zeroth bunch...
    // ... i.e., bunch r=s at site k=0
    uint64_t k_b = (b_p << 1) + std::popcount((S << 1) - b_p) - 1 - epsilon_k_b;  // Site index of bunch

    return k_b + h;  // Calculate placement site...
    // ... where h.v. h is offset within bunch
}

}  // namespace stretched_algo
}  // namespace dstream
}  // namespace downstream
#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_STRETCHED_ASSIGN_STORAGE_SITE_HPP