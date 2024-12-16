#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_ASSIGN_STORAGE_SITE_HPP

#include <algorithm>
#include <bit>
#include <cstdint>
#include <optional>

namespace downstream {
namespace dstream {
namespace tilted_algo {

inline const uint64_t modpow2(const uint64_t x, const uint64_t n) {
  if (n <= 0)
    return 0;
  return x & (n - 1);
}

const std::optional<uint64_t> tilted_assign_storage_site(const uint64_t S, const uint64_t T) {
  const uint64_t s = std::bit_width(S) - 1;
  const uint64_t t = std::max(std::bit_width(T) - s, uint64_t{0}); // Current epoch
  const uint64_t h = std::countr_zero(T + 1); // Current hanoi value
  const uint64_t i = (h + 1) >= 64 ? 0 : (T >> (h + 1)); // Hanoi value incidence (i.e., num seen)

  const uint64_t blt = std::bit_width(t);                    // Bit length of t
  bool epsilon_tau = std::bit_floor(t << 1) > t + blt; // Correction factor
  const uint64_t tau = blt - epsilon_tau;                    // Current meta-epoch
  const uint64_t t_0 = (uint64_t{1} << tau) - tau; // Opening epoch of meta-epoch
  const uint64_t t_1 = (uint64_t{1} << (tau + 1)) -
                 (tau + 1); // Opening epoch of next meta-epoch
  const bool epsilon_b = t < h + t_0 && h + t_0 < t_1; // Uninvaded correction factor
  const uint64_t B = (S >> (tau + 1 - epsilon_b))
                   ? (S >> (tau + 1 - epsilon_b))
                   : 1; // Num bunches available to h.v.

  const uint64_t b_l = modpow2(i, B); // Logical bunch index...
  // ... i.e., in order filled (increasing nestedness/decreasing init size r)

  // Need to calculate physical bunch index...
  // ... i.e., position among bunches left-to-right in buffer space
  const uint64_t v = std::bit_width(b_l); // Nestedness depth level of physical bunch
  const uint64_t w =
      (S >> v) * (v != 0); // Num bunches spaced between bunches in nest level
  const uint64_t o = w >> 1;     // Offset of nestedness level in physical bunch order
  const uint64_t p =
      b_l - std::bit_floor(b_l); // Bunch position within nestedness level
  const uint64_t b_p = o + w * p;      // Physical bunch index...
  // ... i.e., in left-to-right sequential bunch order

  // Need to calculate buffer position of b_p'th bunch
  const bool epsilon_k_b = (b_l != 0); // Correction factor for zeroth bunch...
  // ... i.e., bunch r=s at site k=0
  const uint64_t k_b = (b_p << 1) + std::popcount((S << 1) - b_p) - 1 -
                 epsilon_k_b; // Site index of bunch

  return k_b + h; // Calculate placement site...
                  // ... where h.v. h is offset within bunch
}

} // namespace tilted_algo
} // namespace dstream
} // namespace downstream

#endif // DOWNSTREAM_DSTREAM_TILTED_ALGO_TILTED_ASSIGN_STORAGE_SITE_HPP