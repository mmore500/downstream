#pragma once
#ifndef DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP
#define DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP

#include <cstdint>
#include <format>
#include <iostream>
#include <string_view>

#include "./dstream/dstream.hpp"

namespace downstream {

template <typename Algo>
inline bool is_algo_op(const std::string_view op_name,
                       const std::string_view target_name) {
  return target_name == std::format("{}.{}", Algo::get_algo_name(), op_name);
}

/**
 * Dispatch an `assign_storage_site` op to the matching algorithm and stream
 * `(S, T)` pairs from stdin through `eval`.
 *
 * `Eval` must expose:
 *   template <template <typename> typename Algo>
 *   void operator()(std::uint64_t S, std::uint64_t T, std::uint64_t Smx);
 *
 * Returns 0 on success, 1 if `target_name` does not match a known algorithm.
 */
template <typename Eval>
int dispatch_assign_storage_site(const std::string_view target_name,
                                 Eval &eval) {
  using namespace downstream::dstream;

  std::uint64_t T, S;

#define DOWNSTREAM_DISPATCH_CASE(Algo, Smx)                        \
  if (is_algo_op<Algo##_algo>("assign_storage_site", target_name)) \
    while (std::cin >> S >> T)                                     \
      eval.template operator()<Algo##_algo_>(S, T, Smx);           \
  else

  DOWNSTREAM_DISPATCH_CASE(circular, 1)
  DOWNSTREAM_DISPATCH_CASE(compressing, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_11_steady_12, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_2_steady_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_2_tilted_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_3_steady_4, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_5_steady_6, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_circular_7_steady_8, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_1_circular_2, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_1_stretched_2, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_1_tilted_2, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_1_tilted_2_circular_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_2_circular_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_steady_2_tilted_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_tilted_1_circular_2, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_tilted_2_circular_3, 1)
  DOWNSTREAM_DISPATCH_CASE(hybrid_0_tilted_2_steady_3, 1)
  DOWNSTREAM_DISPATCH_CASE(steady, 1)
  DOWNSTREAM_DISPATCH_CASE(sticky, 1)
  DOWNSTREAM_DISPATCH_CASE(stretched, 2)
  DOWNSTREAM_DISPATCH_CASE(tilted, 2)
  // Trailing `else` from the macro attaches to this fallback block.
  {
    std::cerr << "Unknown algorithm op: " << target_name << '\n';
    return 1;
  }

#undef DOWNSTREAM_DISPATCH_CASE

  return 0;
}

}  // namespace downstream

#endif  // DOWNSTREAM_DISPATCH_ASSIGN_STORAGE_SITE_HPP
