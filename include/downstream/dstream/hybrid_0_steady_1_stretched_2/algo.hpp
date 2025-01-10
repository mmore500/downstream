#pragma once
#ifndef DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HPP
#define DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HPP

#include "../../auxlib/DOWNSTREAM_TO_STATIC_MEM_FUN.hpp"
#include "./_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_hybrid_0_steady_1_stretched_2 {

namespace _ns = dstream_hybrid_0_steady_1_stretched_2;

struct algo {
  algo() = delete;
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, _assign_storage_site);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, assign_storage_site);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, has_ingest_capacity);
};

}  // namespace dstream_hybrid_0_steady_1_stretched_2
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_HYBRID_0_STEADY_1_STRETCHED_2_ALGO_HPP
